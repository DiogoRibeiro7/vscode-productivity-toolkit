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

# Customization Examples

Tailor the toolkit to your workflows by composing new tasks, chaining automation, and integrating with external services. The scenarios below illustrate common extensions to the baseline configuration.

## 1. Enforce Ruff Linting for Python

Add the snippet below to `.vscode/tasks.json` after installing the toolkit. It reuses the `$toolkit-black` matcher for consistent diagnostics.

```json
{
  "label": "python:lint-ruff",
  "type": "shell",
  "command": "python",
  "args": ["-m", "ruff", "check", "src"],
  "group": "build",
  "problemMatcher": "$toolkit-flake8"
}
```

## 2. Cypress UI Regression Suite

Extend the JavaScript automation with an end-to-end task that launches Cypress in headless mode.

```json
{
  "label": "javascript:test-cypress",
  "type": "shell",
  "command": "npx",
  "args": ["cypress", "run", "--browser", "chrome"],
  "options": {
    "env": {
      "CYPRESS_RECORD_KEY": "${input:cypressRecordKey}"
    }
  },
  "problemMatcher": "$toolkit-jest"
}
```

Define the companion input:

```json
{
  "id": "cypressRecordKey",
  "type": "promptString",
  "description": "Optional Cypress Dashboard record key",
  "default": ""
}
```

## 3. Container Security Gate

Schedule a Docker image scan after build completion by chaining task dependencies.

```json
{
  "label": "docker:scan-trivy",
  "type": "shell",
  "command": "trivy",
  "args": ["image", "--severity", "CRITICAL,HIGH", "${input:dockerImageTag}"],
  "dependsOn": "docker:build",
  "problemMatcher": {
    "owner": "trivy",
    "fileLocation": "absolute",
    "pattern": {
      "regexp": "^(?:(CRITICAL|HIGH|MEDIUM|LOW))\\s+(.*)$",
      "severity": 1,
      "message": 2
    }
  }
}
```

## 4. Remote Codespace Bootstrap

Use the general automation entry-point to pre-load extensions and settings when provisioning a GitHub Codespace.

```json
{
  "label": "toolkit:codespace-bootstrap",
  "type": "shell",
  "command": "bash",
  "args": ["${workspaceFolder}/scripts/install.sh", "--silent", "--extensions"],
  "presentation": {
    "reveal": "always",
    "panel": "shared",
    "focus": false
  }
}
```

## 5. Observability Snapshot

Collect metrics and logs before handing over a build to QA by orchestrating multiple tasks.

```json
{
  "label": "toolkit:observability-snapshot",
  "dependsOn": [
    "python:test-pytest-coverage",
    "javascript:test-unit",
    "docker:scan-trivy"
  ],
  "problemMatcher": []
}
```

## Best Practices

- Document each customization in your repository’s onboarding guide.
- Keep security-sensitive inputs (API keys, tokens) in environment variables and reference them via `${env:VAR}`.
- When possible, upstream generic improvements to the toolkit for community benefit.
