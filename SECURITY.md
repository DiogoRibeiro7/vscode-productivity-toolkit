# Security Policy

## 🛡️ Supported Versions

We actively support the following versions with security updates:

Version | Supported          | End of Support
------- | ------------------ | --------------
1.x.x   | ✅ Fully supported  | TBD
0.x.x   | ⚠️ Limited support | 2025-12-31

## 🚨 Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 📧 Private Disclosure

**DO NOT** open a public issue for security vulnerabilities.

**Email**: <dfr@esmad.ipp.pt>

**Subject**: `[SECURITY] VS Code Productivity Toolkit - [Brief Description]`

### 📋 Required Information

Please include:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and affected components
- **Reproduction**: Step-by-step reproduction instructions
- **Environment**: OS, VS Code version, toolkit version
- **Proof of Concept**: Code/screenshots if applicable
- **Suggested Fix**: If you have recommendations

### ⏱️ Response Timeline

- **24 hours**: Initial acknowledgment
- **72 hours**: Preliminary assessment
- **7 days**: Detailed response with action plan
- **30 days**: Security patch release (if confirmed)

### 🏆 Recognition

We maintain a security hall of fame for responsible disclosure:

- Public recognition (with permission)
- Priority support for future issues
- Contributor status in our community

## 🔒 Security Measures

### Code Security

- **Static Analysis**: Bandit for Python, ESLint for JavaScript
- **Dependency Scanning**: Automated vulnerability detection
- **Code Review**: All contributions require review
- **Automated Testing**: Comprehensive test suite

### Extension Security

- **Permissions**: Minimal required permissions
- **Sandboxing**: No access to sensitive system resources
- **Validation**: Input sanitization and validation
- **Secure Defaults**: Security-first configuration

### Infrastructure Security

- **GitHub Security**: Dependabot, secret scanning enabled
- **CI/CD Security**: Isolated build environments
- **Package Security**: Signed releases when possible

## 🛠️ Security Best Practices for Users

### Installation Security

```bash
# Verify repository authenticity
git clone https://github.com/DiogoRibeiro7/vscode-productivity-toolkit.git
cd vscode-productivity-toolkit

# Check GPG signatures (when available)
git log --show-signature -1

# Use virtual environments for Python
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Configuration Security

- Review all tasks before execution
- Use workspace-specific settings
- Regular backup of configurations
- Monitor extension permissions

### Enterprise Security

- Code review all customizations
- Network security for remote features
- Access control for shared configurations
- Regular security audits

## 🔍 Known Security Considerations

### Current Scope

- **File System Access**: Tasks modify VS Code configurations
- **Command Execution**: Tasks run shell commands
- **Network Access**: Extension marketplace, dependency downloads
- **Privilege Requirements**: Some tasks need elevated permissions

### Mitigations

- **Dry-run Mode**: Preview changes before execution
- **Backup Systems**: Automatic backup of existing configurations
- **Permission Validation**: Clear permission requirements
- **Audit Logging**: Track all toolkit operations

## 📚 Security Resources

- [VS Code Security Guidelines](https://code.visualstudio.com/docs/editor/security)
- [Python Security Best Practices](https://python.org/dev/security/)
- [Node.js Security Checklist](https://nodejs.org/en/docs/guides/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🔄 Security Updates

Subscribe to security notifications:

- Watch this repository for security releases
- Follow [@DiogoRibeiro7](https://github.com/DiogoRibeiro7) for updates
- Join our [discussions](https://github.com/DiogoRibeiro7/vscode-productivity-toolkit/discussions) for announcements

## 📞 Contact Information

**Security Team**: <dfr@esmad.ipp.pt><br>
**Institution**: ESMAD - Instituto Politécnico do Porto<br>
**Response Hours**: Monday-Friday, 9:00-17:00 WET/WEST

--------------------------------------------------------------------------------

_This security policy is effective as of January 2025 and is reviewed quarterly._
