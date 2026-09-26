# Quality assurance

The repository validates Python code, task definitions, install scripts, documentation, and the VS Code extension in GitHub Actions.

| Check | What it runs |
| --- | --- |
| Python QA | `pytest` on Ubuntu, macOS, and Windows with Python 3.10 |
| Security and quality | Bandit, codespell, ShellCheck, and JSON task validation |
| Extension build | TypeScript compile and production dependency audit |
| Extension tests | Node 20 and 22 across supported runners; extension host tests on Linux |
| Documentation | Markdown checks and a strict MkDocs build |

Run the main Python checks locally after installing `requirements.txt`:

```bash
python -m pytest -vv
```

The documentation site uses the optional `docs` dependencies from `pyproject.toml`:

```bash
python -m pip install -e ".[docs]"
mkdocs build --strict
```

The [CI workflow](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/.github/workflows/ci.yml) runs the documentation build on pull requests. The [Pages workflow](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/blob/main/.github/workflows/docs.yml) builds again before publishing from `main`.
