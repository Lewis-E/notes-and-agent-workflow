"""Create, validate, and safely update work.yaml files."""

from __future__ import annotations

import argparse
import copy
import json
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError, ValidationError


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SCHEMA_PATH = SCRIPT_DIR / "work.schema.json"


class WorkYamlError(Exception):
    """A user-facing file, input, or validation error."""


class HelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    """Preserve examples while showing argument defaults."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise WorkYamlError(f"duplicate YAML key: {key!r}")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


class WorkSchema:
    """Load and enforce the canonical work-item JSON Schema."""

    def __init__(self, path: Path = DEFAULT_SCHEMA_PATH) -> None:
        self.path = path.resolve()
        self.definition = self._load_definition()
        self.validator = Draft202012Validator(self.definition, format_checker=FormatChecker())

    def _load_definition(self) -> dict[str, Any]:
        try:
            definition = json.loads(self.path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(definition)
        except OSError as exc:
            raise WorkYamlError(f"cannot read schema {self.path}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise WorkYamlError(f"schema is not valid JSON: {exc}") from exc
        except SchemaError as exc:
            raise WorkYamlError(f"schema is not a valid JSON Schema: {exc.message}") from exc
        return definition

    @property
    def kinds(self) -> tuple[str, ...]:
        return tuple(self.definition["properties"]["kind"]["enum"])

    @property
    def status_fields(self) -> tuple[str, ...]:
        fields = self.definition["properties"]["status"]["properties"]
        return tuple(fields)

    def field_definition(self, field: str) -> dict[str, Any]:
        current = self.definition
        for part in field.split("."):
            properties = current.get("properties", {})
            if part not in properties:
                raise WorkYamlError(f"unknown field: {field}")
            current = properties[part]
        return current

    def validate(self, data: dict[str, Any]) -> None:
        self._validate_with(self.validator, data, "work.yaml")

    def _validate_with(
        self,
        validator: Draft202012Validator,
        data: dict[str, Any],
        label: str,
    ) -> None:
        errors = sorted(validator.iter_errors(data), key=self._error_sort_key)
        if not errors:
            return
        details = "\n".join(f"- {self._error_path(error)}: {error.message}" for error in errors)
        raise WorkYamlError(f"{label} is invalid:\n{details}")

    @staticmethod
    def _error_sort_key(error: ValidationError) -> tuple[list[str], str]:
        return [str(part) for part in error.absolute_path], error.message

    @staticmethod
    def _error_path(error: ValidationError) -> str:
        path = "$"
        for part in error.absolute_path:
            path += f"[{part}]" if isinstance(part, int) else f".{part}"
        return path


class WorkYamlDocument:
    """A schema-valid work.yaml document with transactional mutations."""

    def __init__(self, path: Path, data: dict[str, Any], schema: WorkSchema) -> None:
        self.path = path.resolve()
        self.data = data
        self.schema = schema
        self.schema.validate(self.data)

    @classmethod
    def load(cls, path: Path, schema: WorkSchema) -> WorkYamlDocument:
        resolved_path, data = cls._read_mapping(path)
        return cls(resolved_path, data, schema)

    @staticmethod
    def _read_mapping(path: Path) -> tuple[Path, dict[str, Any]]:
        resolved_path = path.resolve()
        try:
            data = yaml.load(resolved_path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        except FileNotFoundError as exc:
            raise WorkYamlError(f"file not found: {resolved_path}") from exc
        except OSError as exc:
            raise WorkYamlError(f"cannot read {resolved_path}: {exc}") from exc
        except yaml.YAMLError as exc:
            raise WorkYamlError(f"invalid YAML in {resolved_path}: {exc}") from exc
        if not isinstance(data, dict):
            raise WorkYamlError("work.yaml must contain a YAML mapping at its root")
        return resolved_path, data

    @classmethod
    def create(
        cls,
        work_directory: Path,
        schema: WorkSchema,
        *,
        kind: str,
        directories: list[str],
        ticket: str | None = None,
    ) -> WorkYamlDocument:
        work_directory = work_directory.resolve()
        path = work_directory / "work.yaml"
        if path.exists():
            raise WorkYamlError(f"refusing to overwrite existing file: {path}")
        status = {gate: gate == "started" for gate in schema.status_fields}
        data: dict[str, Any] = {
            "schema-version": 2,
            "name": work_directory.name,
            "kind": kind,
            "directories": directories,
            "status": status,
            "current-phase": "started",
            "transition-support": {"gate": "human-context", "current": True},
        }
        if ticket is not None:
            data["ticket"] = ticket
        return cls(path, data, schema)

    def set(self, field: str, raw_values: list[str]) -> None:
        self._reject_transition_owned_field(field)
        field_definition = self.schema.field_definition(field)
        value = self._parse_value(field, raw_values, field_definition)
        candidate = copy.deepcopy(self.data)
        parent, key = self._field_parent(candidate, field)
        parent[key] = value
        self.schema.validate(candidate)
        self.data = candidate

    def transition(self, gate: str, *, support_current: bool = False) -> None:
        gates = self.schema.status_fields
        candidate = copy.deepcopy(self.data)
        if support_current:
            candidate["transition-support"] = {"gate": gate, "current": True}

        support = candidate["transition-support"]
        if support["gate"] != gate or not support["current"]:
            raise WorkYamlError(f"transition support for {gate!r} is stale or missing")

        destination = gates.index(gate)
        missing = [name for name in gates[:destination] if not candidate["status"][name]]
        if missing:
            raise WorkYamlError(
                f"transition prerequisite is incomplete: {missing[0]}"
            )

        current_phase = gates.index(candidate["current-phase"])
        if destination < current_phase:
            candidate["status"] = {
                name: index < destination for index, name in enumerate(gates)
            }
        elif not candidate["status"][gate]:
            candidate["status"][gate] = True
        candidate["current-phase"] = gate
        candidate["transition-support"]["current"] = False
        self.schema.validate(candidate)
        self.data = candidate

    def unset(self, field: str) -> None:
        self._reject_transition_owned_field(field)
        self.schema.field_definition(field)
        candidate = copy.deepcopy(self.data)
        parent, key = self._field_parent(candidate, field)
        if key not in parent:
            raise WorkYamlError(f"field is not set: {field}")
        del parent[key]
        self.schema.validate(candidate)
        self.data = candidate

    @staticmethod
    def _reject_transition_owned_field(field: str) -> None:
        if field == "current-phase" or field == "status" or field.startswith("status."):
            raise WorkYamlError(
                "lifecycle state is transition-owned; use the transition command"
            )

    def write(self) -> None:
        self.schema.validate(self.data)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        content = self._schema_comment() + yaml.safe_dump(
            self.data,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )
        previous_mode = stat.S_IMODE(self.path.stat().st_mode) if self.path.exists() else 0o644
        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                delete=False,
            ) as handle:
                temp_path = Path(handle.name)
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            temp_path.chmod(previous_mode)
            temp_path.replace(self.path)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    def _schema_comment(self) -> str:
        relative_schema = os.path.relpath(self.schema.path, self.path.parent)
        return f"# yaml-language-server: $schema={relative_schema}\n"

    @staticmethod
    def _field_parent(data: dict[str, Any], field: str) -> tuple[dict[str, Any], str]:
        parts = field.split(".")
        parent = data
        for part in parts[:-1]:
            child = parent.get(part)
            if not isinstance(child, dict):
                raise WorkYamlError(f"cannot modify {field}: {part} is not an object")
            parent = child
        return parent, parts[-1]

    @staticmethod
    def _parse_value(field: str, raw_values: list[str], field_definition: dict[str, Any]) -> Any:
        expected_type = field_definition.get("type")
        if expected_type == "array":
            return raw_values
        if len(raw_values) != 1:
            raise WorkYamlError(f"{field} requires exactly one value")
        raw_value = raw_values[0]
        if expected_type == "boolean":
            if raw_value not in {"true", "false"}:
                raise WorkYamlError(f"{field} must be exactly true or false")
            return raw_value == "true"
        if expected_type == "string":
            return raw_value
        raise WorkYamlError(f"cannot set {field}: unsupported schema type {expected_type!r}")


class WorkYamlCli:
    """Command-line interface for schema-safe work.yaml operations."""

    def __init__(self, schema: WorkSchema) -> None:
        self.schema = schema
        self.parser = self._build_parser()

    def run(self, argv: Sequence[str] | None = None) -> int:
        args = self.parser.parse_args(argv)
        if args.command == "create" and args.file is not None:
            self.parser.error("create requires --work-dir; --file cannot be used with create")
        handler = getattr(self, f"_run_{args.command.replace('-', '_')}")
        handler(args)
        return 0

    @staticmethod
    def _target_file(args: argparse.Namespace) -> Path:
        if args.file is not None:
            return args.file
        return args.work_dir / "work.yaml"

    def _run_create(self, args: argparse.Namespace) -> None:
        document = WorkYamlDocument.create(
            args.work_dir,
            self.schema,
            kind=args.kind,
            directories=args.directories,
            ticket=args.ticket,
        )
        document.write()
        print(f"created: {document.path}")

    def _run_validate(self, args: argparse.Namespace) -> None:
        document = WorkYamlDocument.load(self._target_file(args), self.schema)
        print(f"valid: {document.path}")

    def _run_set(self, args: argparse.Namespace) -> None:
        document = WorkYamlDocument.load(self._target_file(args), self.schema)
        document.set(args.field, args.values)
        document.write()
        print(f"updated: {document.path} ({args.field})")

    def _run_transition(self, args: argparse.Namespace) -> None:
        document = WorkYamlDocument.load(self._target_file(args), self.schema)
        document.transition(args.gate, support_current=args.support_current)
        document.write()
        print(f"transitioned: {document.path} ({args.gate})")

    def _run_unset(self, args: argparse.Namespace) -> None:
        document = WorkYamlDocument.load(self._target_file(args), self.schema)
        document.unset(args.field)
        document.write()
        print(f"updated: {document.path} (removed {args.field})")

    def _build_parser(self) -> argparse.ArgumentParser:
        status_list = ", ".join(f"status.{status}" for status in self.schema.status_fields)
        parser = argparse.ArgumentParser(
            prog="work-yaml",
            description="Create and update work.yaml without ever writing a schema-invalid result.",
            epilog="""Examples:
  work-yaml --work-dir work/my-task create --kind workflow --directory notes/workflows
  work-yaml --work-dir work/fix-123 create --kind ticket --ticket https://example.com/TICKET-123 --directory example-org/repo
  work-yaml --work-dir work/my-task validate
  work-yaml --file work/my-task/work.yaml transition plan --support-current
  work-yaml --work-dir work/my-task set directories notes/workflows example-org/repo
  work-yaml --file work/my-task/work.yaml unset ticket

All mutations are validated against work.schema.json before an atomic write. Invalid input leaves the file unchanged.
Run `work-yaml --work-dir DIR COMMAND --help` or `work-yaml --file FILE COMMAND --help` for command-specific details.""",
            formatter_class=HelpFormatter,
        )
        target = parser.add_mutually_exclusive_group(required=True)
        target.add_argument(
            "--work-dir",
            type=Path,
            help="work directory; existing-document commands use DIR/work.yaml",
        )
        target.add_argument("--file", type=Path, help="existing work.yaml path")
        subparsers = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")
        self._add_create_parser(subparsers)
        self._add_validate_parser(subparsers)
        self._add_set_parser(subparsers, status_list)
        self._add_transition_parser(subparsers)
        self._add_unset_parser(subparsers)
        return parser

    def _add_create_parser(self, subparsers: Any) -> None:
        parser = subparsers.add_parser(
            "create",
            help="create WORK_DIRECTORY/work.yaml",
            description="Create a work directory and its initial schema-valid work.yaml. The directory basename becomes `name`; only status.started begins true.",
            epilog="""Examples:
  work-yaml --work-dir work/make-review-agent create --kind workflow --directory notes/workflows
  work-yaml --work-dir work/fix-auth create --kind ticket --ticket https://jira.example/browse/AUTH-123 --directory example-org/service

Repeat --directory when the work affects multiple directories. Existing work.yaml files are never overwritten.""",
            formatter_class=HelpFormatter,
        )
        parser.add_argument("--kind", required=True, choices=self.schema.kinds, help="work item kind")
        parser.add_argument("--directory", dest="directories", action="append", required=True, help="affected directory; repeat for multiple directories")
        parser.add_argument("--ticket", help="optional absolute ticket or epic URL")

    @staticmethod
    def _add_validate_parser(subparsers: Any) -> None:
        parser = subparsers.add_parser(
            "validate",
            help="check an existing work.yaml",
            description="Validate an existing work.yaml against work.schema.json without changing it.",
            epilog="Example:\n  work-yaml --work-dir work/make-review-agent validate",
            formatter_class=HelpFormatter,
        )

    @staticmethod
    def _add_set_parser(subparsers: Any, status_list: str) -> None:
        parser = subparsers.add_parser(
            "set",
            help="set one field if the resulting file is valid",
            description="Set one schema-defined field. The complete result is validated before the file is atomically replaced.",
            epilog=f"""Settable scalar fields include name, kind, ticket, runtime-state, and transition-support fields.
Lifecycle fields (current-phase and {status_list}) are transition-owned and cannot be changed with `set`.
Settable array field: directories (provide one or more values).
Boolean values must be exactly `true` or `false`.

Examples:
  work-yaml --work-dir work/my-task set transition-support.current true
  work-yaml --work-dir work/my-task set kind research
  work-yaml --file work/my-task/work.yaml set ticket https://jira.example/browse/TASK-123
  work-yaml --work-dir work/my-task set directories notes/workflows example-org/repo

To remove the optional ticket field, use `unset`; do not set it to an empty string.""",
            formatter_class=HelpFormatter,
        )
        parser.add_argument("field", help="schema field, using dots for nested fields (for example transition-support.current)")
        parser.add_argument("values", nargs="+", help="one scalar value, or every desired value when setting directories")

    def _add_transition_parser(self, subparsers: Any) -> None:
        parser = subparsers.add_parser(
            "transition",
            help="change lifecycle completion through the gate-only transition authority",
            description="Change lifecycle completion through the gate-only transition authority.",
            epilog="Example:\n  work-yaml --work-dir work/my-task transition human-context --support-current",
            formatter_class=HelpFormatter,
        )
        parser.add_argument("gate", metavar="GATE", choices=self.schema.status_fields, help="completion gate")
        parser.add_argument(
            "--support-current",
            action="store_true",
            help="refresh transition support for GATE as part of this transition",
        )

    @staticmethod
    def _add_unset_parser(subparsers: Any) -> None:
        parser = subparsers.add_parser(
            "unset",
            help="remove an optional field if the result remains valid",
            description="Remove a schema-defined optional field. Required fields and status fields cannot be removed because validation will reject the result.",
            epilog="Example:\n  work-yaml --work-dir work/my-task unset ticket",
            formatter_class=HelpFormatter,
        )
        parser.add_argument("field", help="optional schema field to remove (currently: ticket)")


def main(argv: Sequence[str] | None = None) -> int:
    try:
        return WorkYamlCli(WorkSchema()).run(argv)
    except WorkYamlError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
