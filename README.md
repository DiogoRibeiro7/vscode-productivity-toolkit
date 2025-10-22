# File Location: /
# VS Code Productivity Toolkit - Main README

# 🚀 VS Code Productivity Toolkit

> Enterprise-grade automation toolkit with curated tasks, smart project detection, and seamless VS Code integration.

[![CI](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/workflows/CI/badge.svg)](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![VS Code](https://img.shields.io/badge/VS%20Code-Extension-blue.svg)](https://marketplace.visualstudio.com/items?itemName=diogoribeiro7.smart-task-detector)

## 🎯 What is This?

The VS Code Productivity Toolkit is a comprehensive automation solution that transforms your development workflow by providing:

- **🎪 70+ Ready-to-Use Tasks** across Python, JavaScript, React, Node.js, Docker, and Git
- **🔍 Smart Project Detection** that automatically suggests relevant automation based on your codebase
- **⚡ One-Click Installation** via VS Code extension with intelligent merging
- **🛡️ Enterprise Security** with automated scanning, validation, and backup protection
- **📊 Quality Assurance** with comprehensive testing, linting, and documentation automation

## 🚀 Quick Start

### Option 1: VS Code Extension (Recommended)
1. Install the [Smart Task Detector](https://marketplace.visualstudio.com/items?itemName=diogoribeiro7.smart-task-detector) extension
2. Open your project in VS Code
3. Extension automatically detects your project type and suggests relevant tasks
4. Click "Install Recommended Tasks" to get started instantly

### Option 2: Python CLI
```bash
# Install the toolkit
pip install vscode-productivity-toolkit

# Auto-detect and install tasks for current project
vscode-toolkit install --auto-detect

# Install specific task categories
vscode-toolkit install --categories python-general,docker,git
```

### Option 3: Manual Installation
```bash
# Clone the repository
git clone https://github.com/DiogoRibeiro7/vscode-productivity-toolkit.git
cd vscode-productivity-toolkit

# Run the bootstrap script
python scripts/bootstrap-workspace.py
```

## 📦 What You Get

### 🐍 Python Workflows
- **Code Quality**: Black, isort, flake8, mypy, bandit security scanning
- **Testing**: pytest with coverage, property-based testing, mutation testing
- **Packaging**: setuptools, wheel building, PyPI publishing automation
- **Data Science**: Jupyter notebook automation, profiling, documentation generation

### 🟨 JavaScript/TypeScript Workflows  
- **Quality**: ESLint, Prettier, TypeScript checking, import sorting
- **Testing**: Jest, Mocha, Cypress E2E testing, visual regression testing
- **Building**: Webpack, Rollup, Vite bundling with optimization
- **Dependencies**: npm audit, outdated package detection, license checking

### ⚛️ React Workflows
- **Development**: Component scaffolding, prop-types validation, accessibility testing
- **Storybook**: Component documentation and visual testing automation
- **Performance**: Bundle analysis, lighthouse auditing, performance monitoring
- **PWA**: Service worker generation, manifest validation, offline support

### 🟢 Node.js Workflows
- **Server Development**: Express/Fastify setup, middleware validation, API documentation
- **Database**: Migration management, seed data automation, connection testing
- **Deployment**: Docker containerization, PM2 process management, health checks

### 🐳 Docker Workflows
- **Container Management**: Build, run, debug, and deploy containers with best practices
- **Security**: Image vulnerability scanning, secret detection, compliance checking
- **Orchestration**: Docker Compose automation for complex multi-service applications
- **Optimization**: Multi-stage builds, layer caching, size optimization

### 📊 Git Workflows
- **Quality Gates**: Pre-commit hooks, commit message validation, automated testing
- **Branch Management**: Feature branch automation, merge conflict resolution
- **Release Automation**: Semantic versioning, changelog generation, tag management
- **Collaboration**: PR templates, issue automation, code review workflows

## 👨‍💻 Author

**Diogo Ribeiro**
- 🎓 Master in Mathematics  
- 👨‍🏫 Teacher and Researcher at ESMAD - Escola Superior de Média Arte e Design
- 🔬 Lead Data Scientist at Mysense.ai
- 🔗 ORCID: [0009-0001-2022-7072](https://orcid.org/0009-0001-2022-7072)
- 📧 Email: [dfr@esmad.ipp.pt](mailto:dfr@esmad.ipp.pt)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ **Star this repository if it helps boost your productivity!**
