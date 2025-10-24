# Getting Started with VS Code Productivity Toolkit

Welcome to the VS Code Productivity Toolkit! This guide will help you get up and running quickly with automated development workflows.

## 🚀 Quick Start

### Option 1: VS Code Extension (Recommended)

1. **Install the Extension**
   ```
   ext install diogoribeiro7.smart-task-detector
   ```

2. **Automatic Detection**
   - Open your project in VS Code
   - The extension automatically detects your project type
   - Accept the suggestion to install recommended tasks

3. **Start Using Tasks**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Tasks: Run Task"
   - Choose from your installed automation tasks

### Option 2: Python CLI

1. **Install the toolkit**
   ```bash
   pip install vscode-productivity-toolkit
   ```

2. **Auto-detect and install**
   ```bash
   cd your-project
   vscode-toolkit install --auto-detect
   ```

3. **Run tasks in VS Code**
   - Open VS Code in your project
   - Press `Ctrl+Shift+P` → "Tasks: Run Task"

### Option 3: Bootstrap Script

1. **Clone the repository**
   ```bash
   git clone https://github.com/DiogoRibeiro7/vscode-productivity-toolkit.git
   cd vscode-productivity-toolkit
   ```

2. **Run the bootstrap script**
   ```bash
   cd your-project
   python /path/to/bootstrap-workspace.py
   ```

## 📦 What Gets Installed

The toolkit automatically detects your project type and installs relevant tasks:

### 🐍 Python Projects
- **Code Quality**: Black formatting, isort imports, flake8 linting
- **Testing**: pytest with coverage, property-based testing
- **Security**: bandit security scanning
- **Packaging**: setuptools, wheel building, PyPI publishing

### 🟨 JavaScript/TypeScript Projects
- **Code Quality**: ESLint, Prettier, TypeScript checking
- **Testing**: Jest, Mocha, Cypress E2E testing
- **Building**: Webpack, Rollup, Vite bundling
- **Dependencies**: npm audit, outdated packages, license checking

### ⚛️ React Projects
- **Development**: Component scaffolding, prop-types validation
- **Testing**: Component tests, accessibility testing, visual regression
- **Performance**: Bundle analysis, Lighthouse auditing
- **Storybook**: Component documentation and testing

### 🟢 Node.js Projects
- **Server Development**: Express/Fastify setup, API documentation
- **Database**: Migration management, seed data automation
- **Process Management**: PM2 process management, health checks

### 🐳 Docker Projects
- **Container Management**: Build, run, debug containers
- **Security**: Image vulnerability scanning, secret detection
- **Orchestration**: Docker Compose automation
- **Optimization**: Multi-stage builds, layer analysis

### 📊 Git Projects
- **Quality Gates**: Pre-commit hooks, commit message validation
- **Branch Management**: Feature branch automation
- **Release Automation**: Semantic versioning, changelog generation

## 🎯 Using Tasks

### Running Tasks

1. **Command Palette**
   - `Ctrl+Shift+P` → "Tasks: Run Task"
   - Select your desired task

2. **Keyboard Shortcuts**
   - `Ctrl+Shift+P` → "Tasks: Configure Task"
   - Add keyboard bindings for frequently used tasks

3. **Task Explorer**
   - Open the "Productivity Tasks" view in the Explorer panel
   - Click to run tasks directly

### Task Categories

Tasks are organized by categories for easy discovery:

- **Build**: Compilation, bundling, packaging
- **Test**: Unit tests, integration tests, coverage
- **Quality**: Linting, formatting, security scanning
- **Deploy**: Deployment automation, publishing
- **Maintain**: Cleanup, updates, diagnostics

## ⚙️ Configuration

### Extension Settings

Configure the extension behavior in VS Code settings:

```json
{
  "smartTaskDetector.autoDetect": true,
  "smartTaskDetector.enableNotifications": true,
  "smartTaskDetector.preferredCategories": ["python-general", "git-workflows"]
}
```

### Task Customization

Modify installed tasks in `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Python: Format with Black",
      "type": "shell",
      "command": "black",
      "args": ["--line-length", "88", "."],
      "group": "build"
    }
  ]
}
```

## 🔧 Advanced Usage

### Custom Task Installation

Install specific task categories:

```bash
vscode-toolkit install --categories python-general,docker,git
```

### Remote Task Repository

Use a custom task repository:

```bash
vscode-toolkit install --repository https://your-company.com/tasks
```

### Batch Operations

Install tasks for multiple projects:

```bash
python scripts/bulk-install.py --pattern "projects/*" --types python,docker
```

## 🏗️ Project Structure

After installation, your project will have:

```
your-project/
├── .vscode/
│   ├── tasks.json          # VS Code tasks configuration
│   ├── settings.json       # Project-specific settings
│   └── launch.json         # Debug configurations
├── src/                    # Your source code
└── README.md              # Project documentation
```

## 💡 Tips and Best Practices

### 1. Start with Auto-Detection
Let the toolkit detect your project type automatically. It's designed to be smart about identifying the right tools for your stack.

### 2. Customize Gradually
Start with default tasks and customize them as you learn your workflow preferences.

### 3. Use Task Groups
Leverage VS Code's task groups (build, test) to organize your workflow:
- `Ctrl+Shift+P` → "Tasks: Run Build Task" for build tasks
- `Ctrl+Shift+P` → "Tasks: Run Test Task" for test tasks

### 4. Create Task Dependencies
Chain tasks together for complex workflows:

```json
{
  "label": "Full CI Pipeline",
  "dependsOrder": "sequence",
  "dependsOn": ["Lint", "Test", "Build", "Deploy"]
}
```

### 5. Background Tasks
Use background tasks for file watchers and dev servers:

```json
{
  "label": "Dev Server",
  "isBackground": true,
  "runOptions": {
    "runOn": "folderOpen"
  }
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Tasks not appearing**
   - Check if `.vscode/tasks.json` exists
   - Verify VS Code is in the correct workspace folder
   - Reload VS Code window (`Developer: Reload Window`)

2. **Task execution fails**
   - Ensure required tools are installed (node, python, docker, etc.)
   - Check file permissions
   - Verify working directory in task configuration

3. **Extension not detecting project**
   - Ensure project files are in the workspace root
   - Check file patterns in project detection rules
   - Try manual installation with specific types

### Getting Help

- **Documentation**: Check the [full documentation](docs/)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/issues)
- **Discussions**: Join the conversation on [GitHub Discussions](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/discussions)

## 🎉 Next Steps

Now that you're set up:

1. **Explore Tasks**: Run a few tasks to see the automation in action
2. **Customize Workflow**: Modify tasks to match your preferences
3. **Share with Team**: Commit `.vscode/tasks.json` to share with your team
4. **Stay Updated**: Watch the repository for new task categories and features

Happy coding! 🚀

---

*Created by Diogo Ribeiro - [ESMAD](https://www.esmad.ipp.pt/) | [Mysense.ai](https://mysense.ai/)*
