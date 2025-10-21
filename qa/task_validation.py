"""\
MIT License
Copyright (c) 2025 Diogo Ribeiro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Validation helpers for VS Code task definitions.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence

from jsonschema import Draft7Validator

LOGGER = logging.getLogger("toolkit.qa.tasks")


@dataclass(frozen=True)
class ValidationResult:
    """Represents the validation status of a single task file."""

    path: Path
    is_valid: bool
    errors: Sequence[str]


def load_task_schema(base_path: Path) -> Dict[str, object]:
    """Load the toolkit JSON schema definition."""

    schema_path = base_path / "qa" / "task_schema.json"
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def collect_task_files(base_path: Path) -> List[Path]:
    """Collect all task configuration files within the repository."""

    tasks_dir = base_path / "tasks"
    return sorted(tasks_dir.rglob("*.json"))


def validate_task_file(path: Path, validator: Draft7Validator) -> ValidationResult:
    """Validate a single tasks.json file against the schema."""

    with path.open("r", encoding="utf-8") as handle:
        document = json.load(handle)

    errors = [
        f"{error.message} (at {'/'.join(str(part) for part in error.absolute_path) or '<root>'})"
        for error in sorted(validator.iter_errors(document), key=lambda item: item.path)
    ]
    is_valid = not errors
    if not is_valid:
        LOGGER.error("Validation failed", extra={"extra": {"path": str(path), "errors": errors}})
    return ValidationResult(path=path, is_valid=is_valid, errors=errors)


def validate_tasks(base_path: Path) -> List[ValidationResult]:
    """Validate all task files found within ``base_path``."""

    schema = load_task_schema(base_path)
    validator = Draft7Validator(schema)
    results = [validate_task_file(path, validator) for path in collect_task_files(base_path)]
    return results
