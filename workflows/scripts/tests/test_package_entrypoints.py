from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from notes_workflows import work_yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WRAPPER = PROJECT_ROOT / "scripts" / "work-yaml.py"
VALID_DOCUMENT = Path(__file__).resolve().parent / "fixtures" / "v2-current.yaml"


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def test_package_exposes_cli_and_schema() -> None:
    assert callable(work_yaml.main)
    assert work_yaml.DEFAULT_SCHEMA_PATH.is_file()
    document = work_yaml.WorkYamlDocument.load(VALID_DOCUMENT, work_yaml.WorkSchema())
    assert document.path == VALID_DOCUMENT.resolve()


def test_project_console_entry_point_help_and_validation(tmp_path: Path) -> None:
    executable = shutil.which("work-yaml")
    assert executable is not None

    help_result = run([executable, "--help"], cwd=tmp_path)
    validation_result = run(
        [executable, "--file", str(VALID_DOCUMENT), "validate"], cwd=tmp_path
    )

    assert help_result.returncode == 0, help_result.stderr
    assert help_result.stdout.startswith("usage: work-yaml ")
    assert validation_result.returncode == 0, validation_result.stderr
    assert validation_result.stdout.startswith("valid: ")


def test_executable_wrapper_help_and_validation(tmp_path: Path) -> None:
    assert WRAPPER.stat().st_mode & 0o111

    help_result = run([str(WRAPPER), "--help"], cwd=tmp_path)
    validation_result = run(
        [str(WRAPPER), "--file", str(VALID_DOCUMENT), "validate"], cwd=tmp_path
    )

    assert help_result.returncode == 0, help_result.stderr
    assert help_result.stdout.startswith("usage: work-yaml ")
    assert validation_result.returncode == 0, validation_result.stderr
    assert validation_result.stdout.startswith("valid: ")
