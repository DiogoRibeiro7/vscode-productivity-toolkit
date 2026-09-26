# Customize tasks

An installed `.vscode/tasks.json` is ordinary VS Code configuration. Keep the tasks that suit your project and adjust their commands, arguments, working directories, and problem matchers.

## Add a Python lint task

If Ruff is installed in your project environment, append this object to the `tasks` array:

```json
{
  "label": "python:lint-ruff",
  "type": "shell",
  "command": "python",
  "args": ["-m", "ruff", "check", "."],
  "group": "test",
  "problemMatcher": []
}
```

The empty problem matcher avoids depending on a matcher that may not be defined in your workspace.

## Chain existing tasks

Use the actual labels from your installed configuration in `dependsOn`:

```json
{
  "label": "quality:all",
  "dependsOrder": "sequence",
  "dependsOn": ["python:lint-ruff", "python:test-pytest"],
  "problemMatcher": []
}
```

Check both labels in your `tasks.json`; category definitions can evolve. For commands that need secrets, read them from your environment rather than storing credentials in task JSON.

The [task catalog](task-reference.md) links to current definitions, and the [VS Code task documentation](https://code.visualstudio.com/docs/debugtest/tasks) explains the task schema.
