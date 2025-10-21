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

# Sample Project: React Analytics Dashboard

A React + TypeScript project demonstrating how the toolkit streamlines component development, testing, and performance audits.

## Repository Layout

```text
react-dashboard/
├── public/
├── src/
│   ├── components/
│   ├── hooks/
│   └── pages/
├── stories/
├── package.json
├── vite.config.ts
└── README.md
```

## Recommended Tasks

| Task | Purpose |
| --- | --- |
| `react:component-generate` | Scaffolds typed React components with story and test stubs.
| `react:dev-server` | Launches the Vite development server with hot module reload.
| `react:storybook` | Spins up Storybook for component documentation and visual QA.
| `react:test-components` | Executes Jest + React Testing Library suites with problem matchers.
| `react:bundle-analyze` | Runs `source-map-explorer` to identify bundle growth.
| `react:pwa-audit` | Triggers Lighthouse for PWA readiness scoring.

## Workflow

1. Create new components via `react:component-generate` to ensure consistent structure.
2. Use `react:dev-server` during implementation and `react:storybook` for design reviews.
3. Validate quality with `react:test-components` before raising a pull request.
4. Run `react:bundle-analyze` and `react:pwa-audit` prior to release hardening.
5. Publish to production using your CI/CD system after local checks pass.

## Productivity Impact

| Metric | Without Toolkit | With Toolkit |
| --- | --- | --- |
| Component scaffolding | Manual file creation | Automated with naming conventions |
| Visual regression | Manual screenshot diffing | Storybook review tasks |
| Performance tuning | Ad-hoc lighthouse runs | Dedicated command with captured output |

Use this project as a blueprint for analytics dashboards, design systems, or marketing sites requiring rapid iteration.
