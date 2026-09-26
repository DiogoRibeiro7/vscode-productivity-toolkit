# Development

## Local setup

Clone the repository, create a virtual environment, and install the development and documentation extras:

```bash
python -m venv .venv
python -m pip install -e ".[dev,docs]"
```

Activate `.venv` before running the commands below. The Python package uses setuptools as configured in `pyproject.toml`.

## Verify changes

```bash
python -m pytest -vv
mkdocs build --strict
npm ci --prefix extensions/smart-task-detector
npm run compile --prefix extensions/smart-task-detector
npm run lint --prefix extensions/smart-task-detector
```

The extension tests require a VS Code extension host; CI runs them on Linux under `xvfb`. For installer changes, run the corresponding integration tests on your platform and let the CI matrix cover the others.

## Repository layout

| Path | Purpose |
| --- | --- |
| `toolkit/` | Python CLI, detection, and task installation |
| `tasks/` | Source VS Code task definitions |
| `extensions/smart-task-detector/` | TypeScript extension |
| `scripts/` | Bash, PowerShell, and Python installers |
| `tests/` | Python tests |
| `docs/` | This MkDocs site |

Update examples and task descriptions when behavior changes. Use [Contributing](contributing.md) for pull request guidance.
