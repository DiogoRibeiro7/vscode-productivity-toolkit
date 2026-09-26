# Python CLI

The `vscode-toolkit` command currently implements `detect` and `install`. Run `vscode-toolkit --help` for the current argument list. Other command names displayed by the parser are reserved and do not yet have handlers.

## Detect project types

```bash
vscode-toolkit --workspace /path/to/project detect
vscode-toolkit --workspace /path/to/project detect --json
```

Detection reads workspace indicators such as `pyproject.toml`, `package.json`, `Dockerfile`, and `.git`. It suggests task categories without writing to the workspace.

## Install suggested categories

```bash
vscode-toolkit --workspace /path/to/project install --auto-detect
```

The CLI merges suggested tasks into `.vscode/tasks.json`. An existing configuration is backed up by default. The CLI downloads category definitions from the repository over HTTPS during installation.

## Select categories explicitly

```bash
vscode-toolkit --workspace /path/to/project install --categories python-general,git
```

Choose from `python-general`, `python-data-science`, `javascript-general`, `javascript-node`, `javascript-react`, `docker`, and `git`. The [task catalog](task-reference.md) links to each definition.

The global `--workspace` option belongs before the subcommand. Use `--verbose` before the subcommand when diagnosing an error:

```bash
vscode-toolkit --verbose --workspace /path/to/project detect
```

!!! note "Review before running"

    Task definitions are editable VS Code configuration. The toolkit does not install tools such as Docker, pytest, or npm for your project.
