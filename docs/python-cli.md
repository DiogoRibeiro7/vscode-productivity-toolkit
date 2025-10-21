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

# Python Toolkit Modules

The Python modules provide the backbone of the vscode-productivity-toolkit. They expose a flexible command-line interface (CLI), workspace auditing utilities, and shared logging infrastructure.

## Components

| Module | Description |
| --- | --- |
| `toolkit/cli.py` | Entry point for the CLI. Provides commands for auditing workspaces, exporting configuration, and managing extensions. |
| `toolkit/logging.py` | Configures structured logging with JSON output support and log level management. |
| `tasks/python/workspace_audit.py` | Contains the `WorkspaceAuditor` class used to evaluate VS Code environment health. |

## Usage Examples

```bash
# Display available commands
python -m toolkit.cli --help

# Run a workspace audit
python -m toolkit.cli audit --workspace /path/to/project --output ./reports

# Export curated configuration
python -m toolkit.cli configure --output ./exported-config --force
```

Refer to inline docstrings for advanced integration guidance and extend the CLI by adding new subcommands within `toolkit/cli.py`.
