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

# Frequently Asked Questions

## What operating systems are supported?
The toolkit supports Windows 10+, macOS 11+, and Ubuntu 20.04+ through dedicated installation scripts and cross-platform Python modules.

## Which versions of VS Code are compatible?
The toolkit targets VS Code 1.70.0 and above. New releases maintain backward compatibility wherever feasible.

## Do I need administrative privileges to install the toolkit?
Administrative privileges are not required for most operations. However, installing certain extensions or writing to system-level directories may require elevation. The installers detect and report these cases.

## How is logging configured?
Logging defaults to JSON-formatted output at the INFO level. Users can switch to DEBUG mode via the `--log-level` CLI flag to include stack traces for troubleshooting.

## How does the Smart Task Detector decide which tasks to install?
The extension scans the workspace for indicators such as `pyproject.toml`, `requirements.txt`, `package.json`, or Jupyter notebooks. It then surfaces matching task collections (Python data science, Python general, React, Node) in the status bar and quick pick UI. Installation merges the selected JSON definitions into `.vscode/tasks.json`, creating backups and syncing recommended extensions automatically.

## Can I customize the recommended configuration?
Yes. Export the configuration templates using `python -m toolkit.cli configure --output ./path` and modify the generated files. The CLI validates JSON structure to prevent malformed settings.

## How do I contribute a new feature?
Review `docs/contributing.md` for branching strategy, commit conventions, and testing requirements. Submit a pull request referencing the relevant issue or discussion thread.
