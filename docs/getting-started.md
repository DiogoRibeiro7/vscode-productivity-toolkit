# Getting started

The toolkit installs VS Code task definitions into a workspace's `.vscode/tasks.json`. Review the resulting file before running a task: individual tasks use development tools that must be available in that workspace.

## Python CLI

From a clone of the repository:

```bash
python -m pip install -e .
vscode-toolkit --workspace /path/to/your/project detect
vscode-toolkit --workspace /path/to/your/project install --auto-detect
```

The installer reads the task definitions from this repository's `main` branch over HTTPS and merges them with existing tasks. It creates a backup of an existing `tasks.json` by default. Network access is needed for CLI installation.

To choose collections yourself:

```bash
vscode-toolkit --workspace /path/to/your/project install --categories python-general,git
```

See the [Python CLI guide](python-cli.md) for arguments and supported commands, and the [task catalog](task-reference.md) for category names.

## VS Code extension

The Smart Task Detector extension requires VS Code 1.110 or newer. Install it from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=diogoribeiro7.smart-task-detector) if available for your environment, then open a workspace. Use the command palette's **Detect and Install Tasks** or **Open Task Manager** commands to inspect suggestions.

The extension's source and build instructions are in the [extension directory](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/tree/main/extensions/smart-task-detector). Its recommendations are a starting point; inspect the resulting task configuration before use.

## Local installer scripts

For a local checkout, the Bash and PowerShell installers read task JSON from the checkout. Both require the VS Code `code` command to be available, unless `TOOLKIT_CODE_PATH` points to it.

```bash
bash scripts/install.sh --categories python-general --source-root .
```

```powershell
pwsh -File scripts/install.ps1 -Categories python-general -SourceRoot .
```

Use `--dry-run` in Bash or `-DryRun` in PowerShell to inspect the operation first. The scripts install into your home VS Code configuration, while the Python CLI targets the workspace specified with `--workspace`.

## Run tasks

Open the target workspace in VS Code. Open the command palette and select **Tasks: Run Task**, then choose an installed task. If a task fails, check that its executable and project dependencies are installed. See [Troubleshooting](troubleshooting.md).
