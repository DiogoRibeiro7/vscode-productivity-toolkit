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

# Integration: GitHub Actions

Demonstrate how to mirror toolkit automation inside CI pipelines.

## Workflow Snippet

```yaml
name: toolkit-ci

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  toolkit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - name: Install toolkit dependencies
        run: |
          pip install -r requirements.txt
          npm ci --prefix extensions/smart-task-detector
      - name: Run Python quality gates
        run: |
          python -m black --check src
          python -m pytest --maxfail=1 --disable-warnings -vv
      - name: Run JavaScript quality gates
        run: |
          npm run lint --prefix extensions/smart-task-detector
          npm test --prefix extensions/smart-task-detector
```

## Tips

- Reuse the same commands defined in the VS Code task JSON to guarantee parity between local and CI workflows.
- Cache dependency directories (`~/.cache/pip`, `~/.npm`) for faster builds.
- Surface artefacts (coverage reports, bundle analysis) as workflow upload steps to share across the team.
