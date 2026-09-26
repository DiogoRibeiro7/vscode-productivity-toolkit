# Task catalog

Each collection is a JSON file in the repository's [`tasks/` directory](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/tree/main/tasks). Read the source definition to see its labels, commands, inputs, and problem matchers before installing it.

## Python CLI categories

| Category | Source | Typical purpose |
| --- | --- | --- |
| `python-general` | [Python general](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/python/general.json) | Formatting, tests, typing, and packaging |
| `python-data-science` | [Python data science](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/python/data-science.json) | Notebook and data workflows |
| `javascript-general` | [JavaScript general](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/javascript/general.json) | Formatting, linting, and tests |
| `javascript-node` | [Node.js](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/javascript/node.json) | Server workflows |
| `javascript-react` | [React](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/javascript/react.json) | Frontend workflows |
| `docker` | [Docker general](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/docker/general.json) | Container workflows |
| `git` | [Git workflows](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/git/workflows.json) | Git automation |

These are the category identifiers accepted by `vscode-toolkit install --categories`. Auto-detection recommends a subset based on workspace indicators.

## Additional definitions

The repository also includes [Docker Compose](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/docker/compose.json), [Git hooks](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/git/hooks.json), [backup](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/general/backup.json), and [diagnostics](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/tasks/general/diagnostics.json) definitions. They can be copied or adapted manually; the Python CLI category list above does not expose them directly.

After installation, edit `.vscode/tasks.json` to adapt commands and paths to your project. See [Customization](customization-examples.md) for examples.
