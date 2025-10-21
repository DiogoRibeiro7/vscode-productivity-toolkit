# 🤝 Contributing to VS Code Productivity Toolkit

Thank you for your interest in contributing! This guide will help you get started with contributing to the VS Code Productivity Toolkit.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Setup](#-development-setup)
- [Contributing Guidelines](#-contributing-guidelines)
- [Pull Request Process](#-pull-request-process)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Community](#-community)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## 🚀 Getting Started

### Ways to Contribute

- 🐛 **Bug Reports**: Help us identify and fix issues
- 💡 **Feature Requests**: Suggest new functionality
- 📝 **Documentation**: Improve guides and examples
- 🔧 **Code**: Submit bug fixes and new features
- 🧪 **Testing**: Help improve test coverage
- 🎨 **Design**: Enhance user experience and workflows

### Before You Start

1. **Search existing issues** to avoid duplicates
2. **Read the documentation** to understand the project
3. **Check the roadmap** for planned features
4. **Join discussions** to get community feedback

## 🛠️ Development Setup

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** for version control
- **VS Code** for development (recommended)

### Clone and Setup

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/vscode-productivity-toolkit.git
cd vscode-productivity-toolkit

# Set up the upstream remote
git remote add upstream https://github.com/DiogoRibeiro7/vscode-productivity-toolkit.git

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .[dev,test]

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Setup extension development
cd extensions/smart-task-detector
npm install
npm run compile
cd ../..
```

### Verify Setup

```bash
# Run tests
pytest

# Run linting
black --check .
flake8 .
mypy toolkit qa

# Test extension compilation
cd extensions/smart-task-detector
npm run compile
npm run lint
```

## 📋 Contributing Guidelines

### Branch Strategy

- **`main`**: Production-ready code
- **`develop`**: Integration branch for features
- **`feature/description`**: New features
- **`fix/description`**: Bug fixes
- **`docs/description`**: Documentation updates

### Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes
- `build`: Build system changes

**Examples**:

```
feat(tasks): add Docker security scanning task
fix(cli): resolve workspace path validation issue
docs(readme): update installation instructions
test(extension): add integration tests for task detection
```

### Code Style

#### Python

- **Formatting**: Black with 100 character line length
- **Import sorting**: isort with Black profile
- **Linting**: flake8 with configuration in `pyproject.toml`
- **Type hints**: Required for all public functions
- **Docstrings**: Google style for all modules, classes, and functions

```python
def example_function(param: str, optional: int = 0) -> bool:
    """Example function demonstrating our style.

    Args:
        param: Description of the parameter.
        optional: Optional parameter with default value.

    Returns:
        Boolean result of the operation.

    Raises:
        ValueError: When param is invalid.
    """
    if not param:
        raise ValueError("param cannot be empty")
    return len(param) > optional
```

#### TypeScript (Extension)

- **Formatting**: Prettier with project configuration
- **Linting**: ESLint with TypeScript rules
- **Style**: Follow VS Code extension best practices

#### Documentation

- **Markdown**: Follow markdownlint rules
- **Links**: Use relative links for internal documentation
- **Code blocks**: Always specify language for syntax highlighting

### File Organization

```
📁 New contributions should follow this structure:
├── 📄 Source code in appropriate directories
├── 📄 Tests in tests/ with matching structure
├── 📄 Documentation in docs/ if applicable
└── 📄 Examples in examples/ if relevant
```

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**:

  ```bash
  git fetch upstream
  git checkout main
  git merge upstream/main
  ```

2. **Create a feature branch**:

  ```bash
  git checkout -b feature/your-feature-name
  ```

3. **Make your changes** following the guidelines above

4. **Test thoroughly**:

  ```bash
  # Run all tests
  pytest -v

  # Test extension
  cd extensions/smart-task-detector
  npm test
  npm run compile

  # Run pre-commit checks
  pre-commit run --all-files
  ```

5. **Update documentation** if needed

### Submitting the PR

1. **Push your branch**:

  ```bash
  git push origin feature/your-feature-name
  ```

2. **Create pull request** on GitHub with:

  - **Clear title** following conventional commit format
  - **Detailed description** explaining the changes
  - **Link to issues** being addressed
  - **Testing information** and screenshots if applicable
  - **Breaking changes** clearly documented

### PR Template

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change) 
- [ ] Breaking change (fix or feature that breaks existing functionality)
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. **Automated checks** must pass (CI, pre-commit)
2. **Maintainer review** for code quality and design
3. **Testing verification** in different environments
4. **Documentation review** for clarity and completeness
5. **Approval and merge** by maintainers

## 🧪 Testing

### Test Types

- **Unit tests**: Test individual components (`tests/test_*.py`)
- **Integration tests**: Test component interactions (marked with `@pytest.mark.integration`)
- **Performance tests**: Ensure performance requirements (`tests/test_performance_*.py`)
- **Documentation tests**: Validate links and examples (`tests/test_documentation_*.py`)

### Running Tests

```bash
# All tests
pytest

# Specific test types
pytest -m "not integration"  # Skip integration tests
pytest -m "integration"      # Only integration tests
pytest tests/test_specific.py -v

# With coverage
pytest --cov=toolkit --cov=qa --cov-report=html

# Performance tests
pytest tests/test_performance_benchmarks.py
```

### Writing Tests

- **Test file naming**: `test_<module_name>.py`
- **Test function naming**: `test_<functionality>_<expected_result>`
- **Use fixtures** for common setup
- **Mock external dependencies**
- **Test edge cases** and error conditions

```python
def test_workspace_auditor_validates_extensions(tmp_path):
    """Test that workspace auditor properly validates extensions."""
    # Arrange
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    vscode_dir = workspace / ".vscode"
    vscode_dir.mkdir()

    extensions_file = vscode_dir / "extensions.json"
    extensions_file.write_text('{"recommendations": ["ms-python.python"]}')

    # Act
    auditor = WorkspaceAuditor(
        workspace_path=workspace,
        recommended_extensions=["ms-python.python", "ms-vscode.vscode-json"]
    )
    result = auditor.run()

    # Assert
    assert result["extensionCompliance"]["recommendedMissing"] == ["ms-vscode.vscode-json"]
```

## 📚 Documentation

### Documentation Types

- **API Documentation**: Docstrings in code
- **User Guides**: Step-by-step instructions (`docs/`)
- **Examples**: Real-world usage (`examples/`)
- **Architecture**: Technical design documents
- **Troubleshooting**: Common issues and solutions

### Writing Guidelines

- **Clear and concise**: Use simple language
- **Code examples**: Include working examples
- **Screenshots**: Use for UI-related documentation
- **Link validation**: Ensure all links work
- **Keep updated**: Update docs with code changes

### Documentation Structure

```markdown
# Title (H1)
Brief description and purpose.

## Prerequisites (H2)
What users need before starting.

## Step-by-step Instructions (H2)
### Subsection (H3)
Detailed instructions with code examples.

## Examples (H2)
Real-world usage examples.

## Troubleshooting (H2)
Common issues and solutions.
```

## 🎯 Specific Contribution Areas

### Adding New Task Collections

1. **Create task JSON** in appropriate `tasks/` subdirectory
2. **Follow schema** defined in `qa/task_schema.json`
3. **Add problem matchers** for tool output parsing
4. **Include inputs** for user customization
5. **Write tests** for task validation
6. **Update documentation** with examples

Example task structure:

```json
{
  "_metadata": {
    "license": "MIT License - Copyright (c) 2025 Diogo Ribeiro",
    "maintainer": "Your Name <email@example.com>",
    "description": "Description of task collection",
    "version": "1.0.0"
  },
  "version": "2.0.0",
  "inputs": [
    {
      "id": "inputId",
      "type": "promptString",
      "description": "User-friendly description",
      "default": "default-value"
    }
  ],
  "tasks": [
    {
      "label": "category:task-name",
      "detail": "Human-readable description",
      "type": "shell",
      "command": "command-to-run",
      "args": ["${input:inputId}"],
      "problemMatcher": ["$existing-matcher"],
      "presentation": {
        "reveal": "always",
        "panel": "shared"
      }
    }
  ]
}
```

### Extending the Smart Task Detector

1. **Add detection logic** in `extensions/smart-task-detector/src/extension.ts`
2. **Update project types** in detection rules
3. **Add file patterns** for project identification
4. **Test detection accuracy** with various project structures
5. **Update extension manifest** if needed

### Improving Installation Scripts

1. **Test on target platforms** (Windows, macOS, Linux)
2. **Add error handling** and rollback mechanisms
3. **Improve user feedback** and progress indication
4. **Validate dependencies** before installation
5. **Update documentation** with new features

## 🐛 Bug Reports

### Before Reporting

1. **Search existing issues** for duplicates
2. **Update to latest version** to see if fixed
3. **Test in clean environment** to isolate the issue
4. **Gather debugging information**

### Bug Report Template

```markdown
**Bug Description**
Clear description of what went wrong.

**Steps to Reproduce**
1\. Step one
2\. Step two
3\. Step three

**Expected Behavior**
What should have happened.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 11, macOS 13, Ubuntu 22.04]
- VS Code Version: [e.g., 1.85.0]
- Python Version: [e.g., 3.11.2]
- Toolkit Version: [e.g., 1.0.0]

**Additional Context**
- Error messages or logs
- Screenshots if applicable
- Related configuration files
```

## 💡 Feature Requests

### Before Requesting

1. **Check existing issues** and discussions
2. **Consider the scope** and alignment with project goals
3. **Think about implementation** complexity
4. **Gather community feedback** in discussions

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should this work?

**Alternatives Considered**
Other approaches you've considered.

**Additional Context**
- Use cases and examples
- Mockups or diagrams
- Related features or tools
```

## 🎓 Learning Resources

### Project-Specific

- [VS Code Extension API](https://code.visualstudio.com/api)
- [VS Code Task Reference](https://code.visualstudio.com/docs/editor/tasks)
- [Python Packaging Guide](https://packaging.python.org/)

### Development Best Practices

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)

## 🌟 Recognition

### Contributors

All contributors are recognized in:

- **README.md**: Major contributors section
- **CHANGELOG.md**: Release notes with attribution
- **GitHub**: Contributor insights and statistics

### Becoming a Maintainer

Active contributors may be invited to become maintainers based on:

- **Consistent contributions** over time
- **Code quality** and attention to detail
- **Community engagement** and helpfulness
- **Alignment with project values**

## 🆘 Getting Help

### Channels

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Email**: <dfr@esmad.ipp.pt> for sensitive matters

### Response Times

- **Issues**: Within 48 hours for acknowledgment
- **Pull Requests**: Within 72 hours for initial review
- **Security Issues**: Within 24 hours (see <SECURITY.md>)

## 📞 Contact

**Maintainer**: Diogo Ribeiro<br>
**Email**: <dfr@esmad.ipp.pt><br>
**Institution**: ESMAD - Instituto Politécnico do Porto<br>
**GitHub**: [@DiogoRibeiro7](https://github.com/DiogoRibeiro7)

--------------------------------------------------------------------------------

Thank you for contributing to the VS Code Productivity Toolkit! Your efforts help make development more productive for teams worldwide. 🚀
