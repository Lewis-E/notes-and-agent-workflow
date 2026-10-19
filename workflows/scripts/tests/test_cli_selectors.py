from __future__ import annotations

import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml


VALID_DOCUMENT = Path(__file__).resolve().parent / "fixtures" / "v2-current.yaml"


@pytest.mark.parametrize("selector", ["--work-dir", "--file"])
def test_existing_document_selector_updates_only_the_selected_work_yaml(
    selector: str,
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    tmp_path: Path,
) -> None:
    selected_directory = tmp_path / "selected"
    selected_directory.mkdir()
    selected = selected_directory / "work.yaml"
    other = tmp_path / "other.yaml"
    shutil.copyfile(VALID_DOCUMENT, selected)
    shutil.copyfile(VALID_DOCUMENT, other)
    other_before = other.read_bytes()
    target = selected_directory if selector == "--work-dir" else selected

    result = cli_runner(
        selector,
        str(target),
        "set",
        "ticket",
        "https://example.com/TICKET-123",
    )

    assert result.returncode == 0, result.stderr
    assert yaml.safe_load(selected.read_text(encoding="utf-8"))["ticket"] == (
        "https://example.com/TICKET-123"
    )
    assert other.read_bytes() == other_before


@pytest.mark.parametrize("selector_args", [(), ("both",)])
def test_invalid_existing_document_selector_combinations_do_not_write(
    selector_args: tuple[str, ...],
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    tmp_path: Path,
) -> None:
    work_directory = tmp_path / "selected"
    work_directory.mkdir()
    selected = work_directory / "work.yaml"
    other = tmp_path / "other.yaml"
    shutil.copyfile(VALID_DOCUMENT, selected)
    shutil.copyfile(VALID_DOCUMENT, other)
    before = {path: path.read_bytes() for path in (selected, other)}
    args = (
        ["--work-dir", str(work_directory), "--file", str(other)]
        if selector_args
        else []
    )

    result = cli_runner(
        *args,
        "set",
        "ticket",
        "https://example.com/TICKET-123",
        cwd=work_directory,
    )

    assert result.returncode == 2
    assert {path: path.read_bytes() for path in (selected, other)} == before


@pytest.mark.parametrize("selector_args", [(), ("--file", "candidate.yaml")])
def test_create_rejects_non_work_directory_targets_without_side_effects(
    selector_args: tuple[str, ...],
    cli_runner: Callable[..., subprocess.CompletedProcess[str]],
    tmp_path: Path,
) -> None:
    result = cli_runner(
        *selector_args,
        "create",
        "--kind",
        "workflow",
        "--directory",
        "example-org/example",
        cwd=tmp_path,
    )

    assert result.returncode == 2
    assert list(tmp_path.iterdir()) == []
