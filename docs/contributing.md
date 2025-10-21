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

# Contributing Guide

We welcome contributions that enhance developer productivity, security, and accessibility. Please follow the guidelines below to ensure a smooth review process.

## Code of Conduct

By participating in this project you agree to uphold our values of respect, inclusivity, and professionalism. Reports of unacceptable behavior can be sent to [diogo.debastos.ribeiro@gmail.com](mailto:diogo.debastos.ribeiro@gmail.com).

## Development Workflow

1. **Create an Issue** – Describe the bug or feature request and gather feedback before implementation.
2. **Fork and Branch** – Use descriptive branch names such as `feature/audit-report-export` or `fix/windows-install-path`.
3. **Implement Changes** – Follow the coding standards outlined in the repository README and include comprehensive tests.
4. **Run Tests** – Execute `pytest` and any relevant linters before opening a pull request.
5. **Submit Pull Request** – Reference the related issue, include test evidence, and request a review from maintainers.

## Commit Message Convention

All commits must use the Conventional Commits format:

```text
<type>(<scope>): <description>
```

Valid types include `feat`, `fix`, `docs`, `style`, `refactor`, `test`, and `chore`.

## Pull Request Checklist

- [ ] Tests added or updated.
- [ ] Documentation updated with new behavior.
- [ ] CI workflows pass successfully.
- [ ] No secrets or sensitive data included.

Thank you for helping build a reliable and scalable productivity toolkit!
