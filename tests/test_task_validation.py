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

Schema validation for toolkit task definitions.
"""

from __future__ import annotations

from pathlib import Path

from qa.task_validation import collect_task_files, validate_tasks

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_all_tasks_are_schema_compliant() -> None:
    results = validate_tasks(PROJECT_ROOT)
    invalid = [result for result in results if not result.is_valid]
    assert not invalid, f"Non-compliant tasks detected: {invalid}"


def test_task_labels_are_unique() -> None:
    seen = {}
    for path in collect_task_files(PROJECT_ROOT):
        document = path.read_text(encoding="utf-8")
        # A lightweight duplicate check that relies on label occurrences.
        labels = [line.strip() for line in document.splitlines() if '"label"' in line]
        for entry in labels:
            label = entry.split(":", 1)[1].strip().strip('",')
            key = path
            occurrences = seen.setdefault(key, set())
            assert label not in occurrences, f"Duplicate label {label} detected in {path}"
            occurrences.add(label)
