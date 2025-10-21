<!--
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
-->

# Test Suite

The tests in this directory validate the functionality, resilience, and cross-platform compatibility of the toolkit.

## Structure

- `test_toolkit_cli.py` – Unit tests covering CLI argument parsing, validation, and task orchestration logic.
- `test_install_scripts.py` – Cross-platform smoke tests for Bash, PowerShell, and Python installers with rollback protections.
- `test_task_validation.py` – JSON schema compliance enforcement for all toolkit task definitions.
- `test_documentation_quality.py` – Link checking and fenced code block validation across the documentation set.
- `test_extension_manifest.py` – Static analysis of the Smart Task Detector extension manifest and activation events.
- `test_performance_benchmarks.py` – Performance guardrails ensuring task loading remains within latency budgets.

## Running Tests

```bash
pytest
```

Enable verbose output during debugging:

```bash
pytest -vv --maxfail=1
```

Ensure new features include accompanying tests and maintainers update the coverage thresholds accordingly.
