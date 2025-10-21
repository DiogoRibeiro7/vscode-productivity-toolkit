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

# Sample Project: Python Data Science Workspace

This sample illustrates how the toolkit accelerates exploratory analytics.

## Repository Layout

```text
python-data-science/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_ingest.ipynb
│   └── 02_model.ipynb
├── src/
│   └── pipeline/__init__.py
├── environment.yml
└── README.md
```

## Recommended Tasks

| Task | Purpose |
| --- | --- |
| `python:notebooks-export` | Converts notebooks into version-controlled Python scripts.
| `python:notebooks-clean` | Clears output cells before committing.
| `python:data-profile` | Generates exploratory data analysis reports using `ydata-profiling`.
| `python:test-pytest-coverage` | Executes pytest with HTML coverage reports for reproducibility.
| `python:docs-build` | Builds Sphinx documentation driven by notebooks and docstrings.

## Workflow

1. Activate the conda environment using the generated `environment.yml`.
2. Run `python:notebooks-export` to convert notebooks after major edits.
3. Execute `python:data-profile` to validate datasets before modelling.
4. Use `python:profile-performance` to capture CPU/IO hotspots.
5. Publish documentation with `python:docs-build` for stakeholder review.

## Productivity Impact

| Metric | Without Toolkit | With Toolkit |
| --- | --- | --- |
| Notebook cleanup | Manual per file | `python:notebooks-clean` completes in seconds |
| Data profiling | Custom scripts | Single command with HTML output |
| Docs sync | Ad-hoc | Automated via Sphinx task |

Adopt this structure as a template when seeding new data science repositories.
