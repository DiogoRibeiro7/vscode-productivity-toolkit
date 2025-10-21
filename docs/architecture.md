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

# Architecture Overview

## High-Level Components

```mermaid
graph TD
    A[CLI (Python)] --> B[Workspace Auditing Tasks]
    A --> C[Configuration Exporter]
    A --> D[Extension Manager]
    B --> E[Reports & Recommendations]
    C --> F[VS Code Config Templates]
    D --> G[VS Code CLI]
    H[Install Scripts] --> A
    H --> F
```

### CLI Layer

The CLI orchestrates toolkit capabilities through modular commands. It validates user input, delegates to task modules, and emits structured logs for observability.

### Task Modules

Task modules encapsulate business logic such as workspace audits. They expose predictable interfaces so new tasks can be integrated without modifying the CLI core.

### Configuration Templates

Configuration files in the `settings` directory store curated VS Code settings. The CLI can export these templates or merge them with existing user preferences while respecting accessibility requirements.

### Install Scripts

Shell and PowerShell scripts bootstrap the toolkit, install dependencies, and configure environment variables. They rely on defensive programming practices to guarantee safe rollbacks when failures occur.

## Cross-Cutting Concerns

- **Logging**: Structured logging is managed via the `toolkit.logging` module. Logs default to JSON for easy ingestion by observability stacks.
- **Security**: Input validation, path normalization, and sanitized subprocess invocations defend against command injection and insecure defaults.
- **Testing**: The `tests` directory houses unit tests, while GitHub Actions runs the test suite on every commit.
- **Documentation**: All features include up-to-date documentation to support both new and experienced contributors.
