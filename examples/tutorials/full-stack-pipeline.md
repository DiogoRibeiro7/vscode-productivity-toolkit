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

# Tutorial: Full-Stack Delivery Pipeline

Follow this end-to-end tutorial to bootstrap a React frontend, Node.js API, and Python worker, all orchestrated with toolkit tasks.

## Prerequisites

- Toolkit installed via Smart Task Detector or `scripts/setup.py`
- Docker Desktop running
- npm, pnpm, or yarn configured locally

## Steps

1. **Generate Tasks**
   - Run `Toolkit: Detect Project Tasks` and install React + Node recommendations.

2. **Create Frontend**
   - Execute the `react:component-generate` task to scaffold the initial dashboard view.
   - Start the dev server using `react:dev-server`.

3. **Provision API**
   - Use `javascript:express-dev` (from `node.json`) to run the API server with live reload.
   - Apply database migrations via `javascript:db-migrate`.

4. **Add Background Worker**
   - Author Python jobs under `services/worker` and validate them with `python:test-pytest-coverage`.

5. **Run Integrated Tests**
   - Chain tasks using the composite `toolkit:observability-snapshot` example to gather logs and coverage.

6. **Package for Deployment**
   - Build images using `javascript:docker-build` and `python:docker-build` tasks.
   - Execute `javascript:docker-compose-up` to verify the full stack locally.

7. **Automate CI**
   - Copy the workflow from [`examples/integration/github-actions.md`](../integration/github-actions.md) into `.github/workflows/full-stack.yml`.

## Outcome

You now have a reproducible full-stack pipeline where local tasks, automated tests, and CI commands share a single source of truth.
