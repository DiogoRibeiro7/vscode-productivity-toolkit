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

# Configuration Templates

The configuration files in this directory standardise VS Code experiences across teams and platforms. Metadata embedded in each JSON document captures compatibility guarantees and versioning information.

## Contents

| File | Description |
| --- | --- |
| `settings.json` | Optimised VS Code preferences covering editor ergonomics, security defaults, and accessibility tweaks. |
| `keybindings.json` | Keyboard shortcuts designed for high-throughput development while preserving accessibility. |
| `extensions.json` | Curated extension recommendations and unwanted extension guidance. |

## Usage

```bash
python -m toolkit.cli configure --output ./.vscode --force
```

This command copies all configuration files into the target directory while preserving existing backups. Adjust the JSON values to align with your organisation's standards and submit a pull request with rationale and testing notes.
