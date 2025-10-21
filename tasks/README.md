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

# Toolkit Task Catalogue

This directory curates reusable automation tasks grouped by ecosystem. Each task includes defensive input validation, structured logging, and extensive inline documentation to support enterprise adoption.

## Structure

| Path | Purpose |
| --- | --- |
| `python/` | Python-based modules used directly by the CLI or integrated automation pipelines. |
| `javascript/` | Node.js utilities and VS Code task definitions for front-end and tooling workflows. |
| `docker/` | Container orchestration tasks that standardise dev-container and Docker Compose usage. |
| `git/` | Git automation for repository hygiene, branching policies, and compliance checks. |
| `general/` | Cross-language helpers such as backup routines and environment diagnostics. |

## Authoring Guidelines

1. Include the MIT license header at the top of every file.
2. Use descriptive class names in PascalCase and functions in camelCase.
3. Validate user input aggressively and emit actionable error messages.
4. Provide usage examples or sample command snippets in the relevant subdirectory README.
5. Add unit tests for all critical logic and update the documentation to reflect new capabilities.

Refer to [`python/workspace_audit.py`](python/workspace_audit.py) for an end-to-end example of the expected structure and logging practices.
