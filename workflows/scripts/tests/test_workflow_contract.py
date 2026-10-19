from __future__ import annotations

import copy
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import ANY

import pytest
import yaml

from notes_workflows.work_yaml import WorkSchema, WorkYamlCli, WorkYamlDocument


def test_v2_schema_is_the_minimal_ordered_state_authority(
    sample_schema: dict[str, Any],
    workflow_contracts: dict[str, Any],
    ordered_gates: list[str],
) -> None:
    # init
    required_properties = [
        "schema-version",
        "name",
        "kind",
        "directories",
        "status",
        "current-phase",
        "transition-support",
    ]
    removed_properties = {
        "approvals",
        "evidence-references",
        "repository-pins",
        "role-run-receipts",
    }
    expected_properties = {
        "schema-version": {"const": 2, "description": ANY},
        "status": {
            "type": "object",
            "additionalProperties": False,
            "required": ordered_gates,
            "properties": {gate: {"type": "boolean"} for gate in ordered_gates},
        },
        "runtime-state": {
            "type": "string",
            "enum": workflow_contracts["runtimeStates"],
            "description": ANY,
        },
        "current-phase": {
            "type": "string",
            "enum": ordered_gates,
            "description": ANY,
        },
        "transition-support": {
            "type": "object",
            "additionalProperties": False,
            "required": ["gate", "current"],
            "properties": {
                "gate": {"type": "string", "enum": ordered_gates},
                "current": {"type": "boolean"},
            },
        },
    }

    # work
    actual = {
        "required": sample_schema["required"],
        "properties": {
            property_name: sample_schema["properties"][property_name]
            for property_name in expected_properties
        },
        "removed-properties": removed_properties & sample_schema["properties"].keys(),
    }

    # assert
    assert actual == {
        "required": required_properties,
        "properties": expected_properties,
        "removed-properties": set(),
    }


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("status", id="whole-status"),
        pytest.param("status.plan", id="single-gate"),
        pytest.param("current-phase", id="current-phase"),
    ],
)
def test_generic_set_cannot_mutate_lifecycle_state(
    field: str,
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    work_item_factory: Callable[[], Path],
) -> None:
    # init
    path = work_item_factory()
    before = path.read_bytes()

    # work
    result = cli_runner("--file", str(path), "set", field, "true")

    # assert
    assert result.returncode == 1
    assert result.stderr == "error: lifecycle state is transition-owned; use the transition command\n"

    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "field",
    [
        pytest.param("status", id="whole-status"),
        pytest.param("status.plan", id="single-gate"),
        pytest.param("current-phase", id="current-phase"),
    ],
)
def test_generic_unset_cannot_mutate_lifecycle_state(
    field: str,
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    work_item_factory: Callable[[], Path],
) -> None:
    # init
    path = work_item_factory()
    before = path.read_bytes()

    # work
    result = cli_runner("--file", str(path), "unset", field)

    # assert
    assert result.returncode == 1
    assert result.stderr == "error: lifecycle state is transition-owned; use the transition command\n"
    assert path.read_bytes() == before


def test_create_writes_only_minimal_lifecycle_state(
    work_item_factory: Callable[[], Path],
    ordered_gates: list[str],
) -> None:
    # init
    expected_status = {gate: gate == "started" for gate in ordered_gates}

    # work
    path = work_item_factory()
    persisted = yaml.safe_load(path.read_text(encoding="utf-8"))

    # assert
    assert persisted == {
        "schema-version": 2,
        "name": path.parent.name,
        "kind": "workflow",
        "directories": ["example-org/example"],
        "status": expected_status,
        "current-phase": "started",
        "transition-support": {"gate": "human-context", "current": True},
    }


def test_created_work_item_can_transition_to_human_context(
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    work_item_factory: Callable[[], Path],
) -> None:
    # init
    path = work_item_factory()

    # work
    result = cli_runner("--file", str(path), "transition", "human-context")

    # assert
    persisted = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert result.returncode == 0, result.stderr
    assert persisted["status"]["human-context"] is True
    assert persisted["current-phase"] == "human-context"
    assert persisted["transition-support"] == {
        "gate": "human-context",
        "current": False,
    }


def test_transition_cli_exposes_gate_only_interface(
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
) -> None:
    # init
    expected_usage = "usage: work-yaml transition [-h] [--support-current] GATE"
    forbidden_context = ("approval", "evidence", "receipt", "repository")

    # work
    result = cli_runner("--file", "unused.yaml", "transition", "--help")
    actual = {
        "returncode": result.returncode,
        "usage": result.stdout.splitlines()[0],
        "forbidden-context": {
            context: context in result.stdout.lower() for context in forbidden_context
        },
    }

    # assert
    assert actual == {
        "returncode": 0,
        "usage": expected_usage,
        "forbidden-context": {context: False for context in forbidden_context},
    }


def test_transition_cli_rejects_extra_context_without_writing(
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    work_item_factory: Callable[[], Path],
) -> None:
    # init
    path = work_item_factory()
    before = path.read_bytes()

    # work
    result = cli_runner("--file", str(path), "transition", "human-context", "unexpected-extra")

    # assert
    assert result.returncode == 2

    assert path.read_bytes() == before


def test_forward_transition_persists_state_and_consumes_support(
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    sample_v2_state: dict[str, Any],
    work_yaml_factory: Callable[[dict[str, Any]], Path],
    ordered_gates: list[str],
) -> None:
    # init
    sample_v2_state["transition-support"] = {"gate": "human-context", "current": False}
    path = work_yaml_factory(sample_v2_state)
    expected_status = {
        gate: ordered_gates.index(gate) <= ordered_gates.index("research")
        for gate in ordered_gates
    }

    # work
    result = cli_runner(
        "--file", str(path), "transition", "research", "--support-current"
    )

    # assert
    persisted = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert result.returncode == 0, result.stderr
    assert persisted == {
        **sample_v2_state,
        "status": expected_status,
        "current-phase": "research",
        "transition-support": {"gate": "research", "current": False},
    }


def test_final_review_transition_follows_implementation_directly(
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    sample_v2_state: dict[str, Any],
    work_yaml_factory: Callable[[dict[str, Any]], Path],
    ordered_gates: list[str],
) -> None:
    # init
    implementation = ordered_gates.index("implementation")
    final_review = ordered_gates.index("final-review")
    sample_v2_state["status"] = {
        gate: index <= implementation for index, gate in enumerate(ordered_gates)
    }
    sample_v2_state["current-phase"] = "implementation"
    sample_v2_state["transition-support"] = {"gate": "final-review", "current": True}
    path = work_yaml_factory(sample_v2_state)

    # work
    result = cli_runner("--file", str(path), "transition", "final-review")

    # assert
    persisted = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert result.returncode == 0, result.stderr
    assert persisted["status"] == {
        gate: index <= final_review for index, gate in enumerate(ordered_gates)
    }
    assert persisted["current-phase"] == "final-review"
    assert persisted["transition-support"] == {"gate": "final-review", "current": False}


def test_backward_transition_invalidates_destination_and_later_state(
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    sample_v2_state: dict[str, Any],
    work_yaml_factory: Callable[[dict[str, Any]], Path],
    ordered_gates: list[str],
) -> None:
    # init
    destination_gate = "implementation"
    destination = ordered_gates.index(destination_gate)
    last_completed = ordered_gates.index("final-review")
    sample_v2_state["transition-support"] = {"gate": "research", "current": False}
    sample_v2_state["status"] = {
        gate: index <= last_completed for index, gate in enumerate(ordered_gates)
    }
    sample_v2_state["current-phase"] = "final-review"
    path = work_yaml_factory(sample_v2_state)

    # work
    result = cli_runner(
        "--file", str(path), "transition", destination_gate, "--support-current"
    )

    # assert
    persisted = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert result.returncode == 0, result.stderr
    assert persisted == {
        **sample_v2_state,
        "status": {gate: index < destination for index, gate in enumerate(ordered_gates)},
        "current-phase": destination_gate,
        "transition-support": {"gate": destination_gate, "current": False},
    }


def test_same_gate_replay_preserves_completed_state_and_consumes_support(
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    sample_v2_state: dict[str, Any],
    work_yaml_factory: Callable[[dict[str, Any]], Path],
    ordered_gates: list[str],
) -> None:
    # init
    replayed_gate = "final-review"
    last_completed = ordered_gates.index(replayed_gate)
    sample_v2_state["status"] = {
        gate: index <= last_completed for index, gate in enumerate(ordered_gates)
    }
    sample_v2_state["current-phase"] = replayed_gate
    sample_v2_state["transition-support"] = {"gate": "plan", "current": False}
    path = work_yaml_factory(sample_v2_state)

    # work
    result = cli_runner(
        "--file", str(path), "transition", replayed_gate, "--support-current"
    )

    # assert
    persisted = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert result.returncode == 0, result.stderr
    assert persisted == {
        **sample_v2_state,
        "transition-support": {"gate": replayed_gate, "current": False},
    }


def test_support_current_cli_writes_once_with_support_already_consumed(
    monkeypatch: pytest.MonkeyPatch,
    sample_v2_state: dict[str, Any],
    work_yaml_factory: Callable[[dict[str, Any]], Path],
) -> None:
    # init
    sample_v2_state["transition-support"] = {"gate": "human-context", "current": False}
    path = work_yaml_factory(sample_v2_state)
    writes: list[dict[str, Any]] = []
    original_write = WorkYamlDocument.write

    def observe_write(document: WorkYamlDocument) -> None:
        writes.append(copy.deepcopy(document.data))
        original_write(document)

    monkeypatch.setattr(WorkYamlDocument, "write", observe_write)

    # work
    result = WorkYamlCli(WorkSchema()).run(
        ["--file", str(path), "transition", "research", "--support-current"]
    )

    # assert
    assert result == 0
    assert len(writes) == 1
    assert writes[0]["current-phase"] == "research"
    assert writes[0]["transition-support"] == {"gate": "research", "current": False}
    assert yaml.safe_load(path.read_text(encoding="utf-8")) == writes[0]


@pytest.mark.parametrize(
    "gate,transition_support,additional_completed_gates,support_current,expected_error",
    [
        pytest.param(
            "research",
            {"gate": "human-context", "current": True},
            (),
            False,
            "error: transition support for 'research' is stale or missing\n",
            id="mismatched-support-without-flag",
        ),
        pytest.param(
            "plan",
            {"gate": "research", "current": False},
            ("research",),
            True,
            "error: transition prerequisite is incomplete: context-and-requirements\n",
            id="missing-prerequisite",
        ),
    ],
)
def test_transition_rejection_preserves_file(
    gate: str,
    transition_support: dict[str, Any],
    additional_completed_gates: tuple[str, ...],
    support_current: bool,
    expected_error: str,
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    sample_v2_state: dict[str, Any],
    work_yaml_factory: Callable[[dict[str, Any]], Path],
) -> None:
    # init
    sample_v2_state["transition-support"] = transition_support
    for completed_gate in additional_completed_gates:
        sample_v2_state["status"][completed_gate] = True
    path = work_yaml_factory(sample_v2_state)
    before = path.read_bytes()

    # work
    args = ["--file", str(path), "transition", gate]
    if support_current:
        args.append("--support-current")
    result = cli_runner(*args)

    # assert
    assert result.returncode == 1
    assert result.stderr == expected_error

    assert path.read_bytes() == before
