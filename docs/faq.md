# Frequently asked questions

## Where are tasks installed?

The Python CLI writes to the selected workspace's `.vscode/tasks.json`. The Bash and PowerShell scripts install under the user's home VS Code configuration. See [Getting started](getting-started.md) for the commands.

## Which VS Code version does the extension require?

The extension manifest declares `^1.110.0`. The JSON task definitions themselves are VS Code configuration and can be inspected independently of the extension.

## Does the toolkit install Python, Docker, or npm?

No. Task definitions call tools already installed in your development environment.

## Can I choose collections without detection?

Yes. Use `vscode-toolkit --workspace /path/to/project install --categories python-general,git`. See the [task catalog](task-reference.md).

## Can I review changes before installing?

The Bash and PowerShell scripts have dry-run options. The Python CLI backs up an existing `tasks.json` by default, but does not currently provide a dry-run command. Use version control for the workspace configuration and inspect the generated file.

## How do I report a problem?

Open a [GitHub issue](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/issues) with the command, operating system, version, and relevant error output. Remove credentials and personal paths from logs first.
