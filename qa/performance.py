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

Performance benchmarking helpers for toolkit operations.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

from qa.task_validation import collect_task_files


@dataclass(frozen=True)
class BenchmarkResult:
    """Represents a performance benchmark output."""

    name: str
    duration: float
    passed: bool


def benchmark_task_loading(base_path: Path, budget_seconds: float = 0.5) -> BenchmarkResult:
    """Measure the time required to load all task definitions."""

    start = time.perf_counter()
    aggregate: List[dict] = []
    for path in collect_task_files(base_path):
        with path.open("r", encoding="utf-8") as handle:
            aggregate.append(json.load(handle))
    duration = time.perf_counter() - start
    return BenchmarkResult(name="task-loading", duration=duration, passed=duration <= budget_seconds)
