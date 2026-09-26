<div class="toolkit-hero" markdown="1">

# VS Code tasks for your workspace

Detect a project's tools, choose the task collections you need, and keep the resulting `.vscode/tasks.json` under your control.

[Get started](getting-started.md){ .md-button .md-button--primary }
[Browse task collections](task-reference.md){ .md-button }

</div>

<div class="toolkit-cards" markdown="1">

<div markdown="1">

### Detect

The Python CLI and VS Code extension identify project indicators such as `pyproject.toml` and `package.json`.

</div>

<div markdown="1">

### Install

Choose task definitions for Python, JavaScript, React, Node.js, Docker, and Git workflows.

</div>

<div markdown="1">

### Adapt

Review the generated VS Code tasks, keep the ones that fit your project, and add your own commands.

</div>

</div>

## Work with the toolkit

The repository includes a Python CLI, a VS Code extension, and Bash, PowerShell, and Python install scripts. Each provides a different route to the task definitions in `tasks/`. Start with the [installation guide](getting-started.md), then use the [task catalog](task-reference.md) to inspect the source JSON before installing.

Tasks call tools already available in your project environment. For example, a task that runs `pytest` requires `pytest` to be installed in that project. The [customization guide](customization-examples.md) shows how to adjust these commands.
