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

# Installation and Setup Scripts

This directory automates toolkit onboarding across supported platforms.

## Available Scripts

| Script | Platform | Description |
| --- | --- | --- |
| `install.sh` | Linux/macOS | POSIX-compliant installer that applies VS Code settings and extensions. |
| `install.ps1` | Windows / PowerShell Core | PowerShell installer with rollback support and structured logging. |
| `setup.py` | Cross-platform | Python utility to install dependencies and export configuration via the CLI. |

## Usage

```bash
./scripts/install.sh
```

```powershell
./scripts/install.ps1
```

```bash
python ./scripts/setup.py --install-deps --configure --force
```

Consult inline comments for advanced flags and environment variables. Always review the scripts before execution in production environments.
