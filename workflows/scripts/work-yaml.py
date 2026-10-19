#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jsonschema[format]>=4.23,<5",
#   "PyYAML>=6,<7",
# ]
# ///
"""Executable compatibility wrapper for the canonical work-yaml package."""

from __future__ import annotations

import sys
from pathlib import Path

# Keep this source-tree wrapper independently runnable without installing the project.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from notes_workflows.work_yaml import main


if __name__ == "__main__":
    raise SystemExit(main())
