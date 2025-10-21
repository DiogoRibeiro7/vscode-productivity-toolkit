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

# Troubleshooting Guide

## Installation Issues

### Symptom
Installer exits with `command not found: code`.

### Resolution
Ensure the VS Code command line interface is installed. In VS Code, open the Command Palette and run `Shell Command: Install 'code' command in PATH`. Re-run the installer afterwards.

### Symptom
PowerShell script reports insufficient execution policy rights.

### Resolution
Launch PowerShell as Administrator and execute `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` before rerunning the installer.

## CLI Errors

### Symptom
`python -m toolkit.cli` fails with `Workspace path is invalid`.

### Resolution
Verify that the `--workspace` argument points to an existing directory. Use absolute paths to avoid ambiguity on Windows environments.

### Symptom
CLI commands hang when interacting with VS Code.

### Resolution
Set the environment variable `TOOLKIT_CODE_PATH` to the absolute path of the VS Code binary if it is installed in a non-standard location. Commands include a default timeout of 25 seconds to prevent indefinite waits.

## Logging and Reports

### Symptom
Generated audit report is empty.

### Resolution
Run the CLI with `--log-level DEBUG` to capture additional diagnostic output. Confirm the workspace contains a `.vscode` directory and relevant configuration files.

If issues persist, open a GitHub issue including logs, OS details, and toolkit version.
