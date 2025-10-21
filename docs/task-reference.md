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

# Task Reference

This reference summarises the curated task suites provided by the toolkit. Tasks are grouped by domain with links to their JSON definitions for deeper inspection.

## Python

| Collection | File | Highlights |
| --- | --- | --- |
| Data Science | [`tasks/python/data-science.json`](../tasks/python/data-science.json) | Notebook conversion, coverage, profiling, Sphinx docs, and dependency export prompts. |
| General | [`tasks/python/general.json`](../tasks/python/general.json) | Black, isort, flake8, pylint, mypy, bandit, packaging, Docker builds, git automation. |

## JavaScript & TypeScript

| Collection | File | Highlights |
| --- | --- | --- |
| React | [`tasks/javascript/react.json`](../tasks/javascript/react.json) | Component scaffolding, Vite/CRA dev servers, Storybook, Jest, Lighthouse, bundle analysis. |
| Node Services | [`tasks/javascript/node.json`](../tasks/javascript/node.json) | Express dev, Prisma migrations, Newman API tests, Docker builds, npm publish, Clinic profiling. |
| General | [`tasks/javascript/general.json`](../tasks/javascript/general.json) | ESLint/Prettier, pnpm/yarn/npm orchestration, tsconfig builds, vitest/jest coverage, dependency hygiene. |

## Cross-Cutting

| Collection | Location | Highlights |
| --- | --- | --- |
| Git Automation | [`tasks/git/README.md`](../tasks/git/README.md) | Conventional commit helpers, branch hygiene, release scaffolding. |
| General Ops | [`tasks/general/README.md`](../tasks/general/README.md) | Shell health checks, changelog generation, repo analytics. |
| Docker | [`tasks/docker/README.md`](../tasks/docker/README.md) | Compose orchestration, vulnerability scanning patterns, container hygiene tips. |

## Inputs & Problem Matchers

Each JSON file exposes `inputs` arrays that drive interactive prompts. The Smart Task Detector and the VS Code UI resolve these inputs at runtime.

The toolkit ships with custom problem matchers contributed by the Smart Task Detector extension:

- `$toolkit-black`, `$toolkit-isort`, `$toolkit-flake8`, `$toolkit-pylint`
- `$toolkit-mypy`, `$toolkit-pytest`
- `$toolkit-eslint`, `$toolkit-jest`, `$toolkit-npm-audit`

Apply these by referencing their identifiers in any bespoke tasks you author or extend.

## Extending Tasks

1. Copy an existing task block into `.vscode/tasks.json`.
2. Change the `label`, `command`, and `args` to match your tool.
3. Reference one of the problem matchers above or embed a custom object inline.
4. Commit changes alongside documentation updates so the team understands the automation.

For concrete examples, head to [Customization Examples](./customization-examples.md).
