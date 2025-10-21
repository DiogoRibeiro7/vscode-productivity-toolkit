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

# Workspace Bootstrap

This recipe demonstrates how to create a new repository and prepare a consistent VS Code environment using the toolkit.

## Steps

1. **Clone the template**
   ```bash
   git clone https://github.com/DiogoRibeiro7/vscode-productivity-toolkit.git my-new-project
   cd my-new-project
   ```
2. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Apply configuration**
   ```bash
   python -m toolkit.cli configure --output .vscode --force
   ```
4. **Review the audit report**
   ```bash
   python -m toolkit.cli audit --workspace . --extensions settings/extensions.json
   ```
5. **Share results** – Commit `.vscode` and the generated audit report to track workspace health over time.

## Troubleshooting

- Run `pytest -vv` to verify the CLI behaves as expected before onboarding additional teammates.
- Use the `--plain-logs` flag if your terminal does not support JSON-formatted logs.
