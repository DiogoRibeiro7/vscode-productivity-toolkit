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

# Development Guide

This document explains how to work with the toolkit source code, run tests, and validate documentation updates.

## Local Environment Setup

1. Create a Python virtual environment with `python -m venv .venv`.
2. Activate the environment and install dependencies via `pip install -r requirements.txt`.
3. Install optional tooling such as `jq` (for shell installers) and the VS Code `code` CLI.

## Running Tests

```bash
pytest --maxfail=1 --disable-warnings -vv
npm install --prefix extensions/smart-task-detector
npm run compile --prefix extensions/smart-task-detector
```

All new features require unit tests. Integration tests should be added when functionality spans multiple modules (e.g., CLI + task module).

## Formatting & Linting

- Follow PEP 8 and use descriptive camelCase function names in Python modules.
- Prefer `ruff` or `flake8` for linting; include commands and configuration in follow-up contributions.
- PowerShell scripts must pass `PSScriptAnalyzer` validation with the default rule set.

## Directory Overview

| Path | Description |
| --- | --- |
| `toolkit/` | Python package exposing the CLI entry point and logging utilities. |
| `tasks/` | Modular automation organised by ecosystem. Python tasks can be imported directly into the CLI. |
| `extensions/` | VS Code extensions, including the Smart Task Detector TypeScript project. Run `npm run compile` before committing. |
| `scripts/` | Installation and environment bootstrap scripts for Bash, PowerShell, and Python. |
| `settings/` | VS Code configuration templates exported by the CLI. |
| `snippets/` | Shared snippet packs that accelerate common tasks. |

Review each directory README for detailed contribution notes before submitting pull requests.
