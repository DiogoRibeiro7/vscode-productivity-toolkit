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

# Getting Started

Welcome to the **VS Code Productivity Toolkit**. This guide walks you through installation, configuration, and the first productivity boosts you can expect.

## Prerequisites

- VS Code **1.70.0+**
- Python **3.8+**, Node.js **16+**, and Git available on your `PATH`
- PowerShell **5.1+** (Windows) or Bash/Zsh (macOS/Linux)
- Internet connectivity to download extensions and dependencies

## Installation Options

### 1. Guided Python Installer (Recommended)

```bash
python scripts/setup.py
```

- Launches a Tkinter-based wizard that surfaces task categories, previews the commands that will be installed, and applies them with rollback safeguards.
- Automatically synchronises recommended extensions and can run silently using `--silent`.

### 2. Platform-Specific Scripts

- **Windows**: `powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1`
- **macOS/Linux**: `bash ./scripts/install.sh`

Both scripts prompt for the task suites you want (Python, JavaScript, Docker, Git, General) and protect your existing `.vscode/tasks.json` by creating timestamped backups.

### 3. Smart Task Detector Extension

1. Open the repository in VS Code.
2. Run the command palette entry **Toolkit: Detect Project Tasks**.
3. Accept the installation prompt to merge the recommended task collections.

> The extension reads from the repository’s `tasks/` directory, so you always install the latest curated automations.

## Post-Installation Checklist

- Confirm `.vscode/tasks.json` and `.vscode/extensions.json` contain the expected updates.
- Run `Tasks: Run Task` in VS Code to explore the new task groups.
- Review `settings/settings.json` for recommended editor defaults (format on save, diagnostics grouping, etc.).
- Browse `docs/task-reference.md` to understand the commands and when to use them.

## Next Steps

- Visit the [Task Reference](./task-reference.md) for deep dives into each automation suite.
- Explore [`examples/`](../examples/README.md) to see the toolkit applied in real projects.
- Join discussions, file issues, or submit pull requests through the [GitHub contribution workflow](./contributing.md).
