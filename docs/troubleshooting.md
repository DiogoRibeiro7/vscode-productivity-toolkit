# Troubleshooting

## `code` command is not found

The local Bash and PowerShell installers require the VS Code CLI. Add `code` to your `PATH` or set `TOOLKIT_CODE_PATH` to its executable. In VS Code on macOS, use the command palette action **Shell Command: Install 'code' command in PATH**.

## Workspace path is rejected

Pass an existing directory with the global option before the subcommand:

```bash
vscode-toolkit --workspace /path/to/project detect
```

## No project type is detected

Use explicit categories after checking the [task catalog](task-reference.md):

```bash
vscode-toolkit --workspace /path/to/project install --categories python-general
```

## A task cannot find an executable

Install the tool required by that task in your project environment. Open `.vscode/tasks.json` and inspect its `command` and `args` fields.

## A task or extension installation fails

Run the CLI with the global `--verbose` flag, or use the script's dry-run option to inspect the planned actions. If the Python CLI cannot download a category, check HTTPS access to `raw.githubusercontent.com`.

If the issue persists, [report it](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/issues) with the failing command and relevant logs.
