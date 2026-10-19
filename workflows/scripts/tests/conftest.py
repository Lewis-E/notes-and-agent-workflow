from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "work-yaml.py"
SCHEMA = Path(__file__).resolve().parents[2] / "src" / "notes_workflows" / "work.schema.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.fixture
def cli_runner() -> Callable[..., subprocess.CompletedProcess[str]]:
    return run


@pytest.fixture
def work_root(tmp_path: Path) -> Path:
    root = tmp_path / "work-root"
    root.mkdir()
    return root


@pytest.fixture(scope="session")
def workflow_contracts() -> dict[str, Any]:
    return json.loads((FIXTURES / "contracts.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def ordered_gates(workflow_contracts: dict[str, Any]) -> list[str]:
    return workflow_contracts["orderedGates"]


@pytest.fixture(scope="session")
def sample_schema() -> dict[str, Any]:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


@pytest.fixture
def sample_v2_state() -> dict[str, Any]:
    return yaml.safe_load((FIXTURES / "v2-current.yaml").read_text(encoding="utf-8"))


@pytest.fixture
def work_item_factory(
    cli_runner: Callable[..., subprocess.CompletedProcess[str]], work_root: Path
) -> Callable[[], Path]:
    created = 0

    def create() -> Path:
        nonlocal created
        created += 1
        work_directory = work_root / f"created-work-{created}"
        result = cli_runner(
            "--work-dir",
            str(work_directory),
            "create",
            "--kind",
            "workflow",
            "--directory",
            "example-org/example",
        )
        assert result.returncode == 0, result.stderr
        return work_directory / "work.yaml"

    return create


@pytest.fixture
def work_yaml_factory(work_root: Path) -> Callable[[dict[str, Any]], Path]:
    created = 0

    def create(data: dict[str, Any]) -> Path:
        nonlocal created
        created += 1
        path = work_root / f"work-{created}.yaml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    return create
