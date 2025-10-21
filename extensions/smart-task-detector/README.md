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

# Smart Task Detector Extension

The Smart Task Detector augments the **vscode-productivity-toolkit** by automatically discovering project characteristics, surfacing the most relevant task collections, and installing curated automation with a single click.

## Features

- 🔍 **Auto-detects** Python, data science, React, and Node.js workspaces using heuristics that inspect dependencies, notebooks, and source layout.
- ⚙️ **Status bar recommendations** summarise relevant task collections and open an installation quick pick on click.
- ⚡ **One-click installation** merges toolkit task definitions into `.vscode/tasks.json`, creating timestamped backups before changes are applied.
- 🧩 **Extension syncing** updates `.vscode/extensions.json` with the recommended marketplace extensions required by the selected workflows.
- 🛡️ **Problem matcher registry** contributes reusable diagnostics for the toolkit’s linters, testers, and security analyzers.
- 🗒️ **Verbose logging** via a dedicated output channel that can be toggled through the `vscodeProductivityToolkit.enableLogging` setting.

## Usage

1. Install the toolkit repository or package and open it in VS Code.
2. Run the command palette entry **Toolkit: Detect Project Tasks** to trigger detection manually, or rely on automatic activation on startup.
3. Review suggested collections from the status bar or `Toolkit: Show Task Recommendations` quick pick.
4. Select the desired task suites and press **Install** to merge them into your workspace.

> The detector respects the `vscodeProductivityToolkit.autoInstall` configuration flag. When enabled, a confirmation prompt appears after each detection run offering immediate installation.

## Development

```bash
cd extensions/smart-task-detector
npm install
npm run compile
```

The compiled JavaScript is stored in `dist/extension.js`. Update the TypeScript source and re-run the build to regenerate the output before committing.

## Telemetry and Privacy

The extension does **not** collect telemetry or transmit workspace information outside of the local machine. Detection happens entirely within the VS Code runtime and only reads repository files necessary to identify project types.

## Support

If you encounter issues or have ideas for new detection heuristics, please open a discussion or issue on the main repository. Contributions are welcome via pull requests aligned with the project’s contribution guidelines.
