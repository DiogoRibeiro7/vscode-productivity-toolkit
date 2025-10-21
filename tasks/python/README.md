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

# Python Tasks

Python tasks power advanced automation scenarios and are imported directly by the toolkit CLI. Each module exposes well-typed classes with clear `run` methods and structured logging.

## Available Tasks

- `workspace_audit.py` – Audits a VS Code workspace for configuration drift, missing extensions, and potential optimisations.

## Usage

```python
from tasks.python.workspace_audit import WorkspaceAuditor

auditor = WorkspaceAuditor(
    workspace_path=Path("/path/to/workspace"),
    recommended_extensions=["ms-python.python"],
)
print(auditor.run())
```

## Creating New Tasks

1. Start with a descriptive class name (e.g., `DependencyComplianceTask`).
2. Require keyword-only arguments for clarity and forward compatibility.
3. Log progress with `toolkit.logging.get_logger` at the `INFO` level by default.
4. Add unit tests in the `tests/` directory and update this README with usage examples.
