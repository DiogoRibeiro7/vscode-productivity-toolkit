# Task Reference Documentation

This document provides a comprehensive reference for all tasks available in the VS Code Productivity Toolkit.

## 📋 Task Categories

### 🐍 Python Development

#### General Python Tasks (`python/general.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| Python: Format with Black | `black .` | Format code using Black formatter | build |
| Python: Sort Imports | `isort .` | Sort and organize imports | build |
| Python: Lint with flake8 | `flake8 .` | Check code style and quality | test |
| Python: Type Check with mypy | `mypy .` | Static type checking | test |
| Python: Run Tests | `pytest` | Execute test suite | test |
| Python: Test with Coverage | `pytest --cov` | Run tests with coverage report | test |
| Python: Security Check | `bandit -r .` | Security vulnerability scan | test |
| Python: Install Dependencies | `pip install -r requirements.txt` | Install project dependencies | build |
| Python: Create Virtual Environment | `python -m venv venv` | Create isolated environment | build |
| Python: Activate Virtual Environment | `source venv/bin/activate` | Activate virtual environment | build |
| Python: Generate Requirements | `pip freeze > requirements.txt` | Export current dependencies | build |
| Python: Build Package | `python setup.py sdist bdist_wheel` | Build distribution packages | build |

#### Data Science Tasks (`python/data-science.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| Jupyter: Start Lab | `jupyter lab` | Launch Jupyter Lab | build |
| Jupyter: Start Notebook | `jupyter notebook` | Launch Jupyter Notebook | build |
| Jupyter: Convert to Python | `jupyter nbconvert --to script *.ipynb` | Convert notebooks to Python | build |
| Jupyter: Convert to HTML | `jupyter nbconvert --to html *.ipynb` | Convert notebooks to HTML | build |
| Data: Profile Dataset | `python -m pandas_profiling` | Generate data profile report | test |
| Data: Validate Schema | `great_expectations checkpoint run` | Validate data quality | test |
| ML: Train Model | `python train.py` | Train machine learning model | build |
| ML: Evaluate Model | `python evaluate.py` | Evaluate model performance | test |
| ML: Export Model | `python export_model.py` | Export trained model | build |
| Analysis: Generate Report | `python generate_report.py` | Create analysis report | build |
| Viz: Generate Plots | `python create_visualizations.py` | Generate data visualizations | build |
| Docs: Build Sphinx | `sphinx-build docs docs/_build` | Build documentation | build |
| Environment: Export Conda | `conda env export > environment.yml` | Export conda environment | build |
| Data: Download Datasets | `python download_data.py` | Download required datasets | build |
| Notebook: Run All | `jupyter nbconvert --execute *.ipynb` | Execute all notebooks | test |

### 🟨 JavaScript Development

#### General JavaScript/TypeScript Tasks (`javascript/general.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| ESLint: Check Code Quality | `npx eslint .` | Lint JavaScript/TypeScript code | test |
| ESLint: Fix Auto-fixable Issues | `npx eslint . --fix` | Auto-fix linting issues | build |
| Prettier: Format Code | `npx prettier --write **/*.{js,jsx,ts,tsx}` | Format code with Prettier | build |
| Prettier: Check Formatting | `npx prettier --check **/*.{js,jsx,ts,tsx}` | Check code formatting | test |
| TypeScript: Type Check | `npx tsc --noEmit` | Type checking without compilation | test |
| Jest: Run All Tests | `npm test` | Execute test suite | test |
| Jest: Run Tests with Coverage | `npm run test:coverage` | Run tests with coverage | test |
| Jest: Run Tests in Watch Mode | `npm run test:watch` | Watch mode testing | test |
| Build: Production Bundle | `npm run build` | Create production build | build |
| Build: Development Bundle | `npm run build:dev` | Create development build | build |
| Start: Development Server | `npm start` | Start development server | build |
| Dependencies: Check for Updates | `npm outdated` | Check for package updates | test |
| Dependencies: Security Audit | `npm audit` | Security vulnerability check | test |
| Dependencies: Fix Vulnerabilities | `npm audit fix` | Fix security vulnerabilities | build |
| License: Check Dependencies | `npx license-checker --summary` | Check dependency licenses | test |

#### Node.js Server Tasks (`javascript/node.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| Node: Start Development Server | `npm run dev` | Start development server | build |
| Node: Start Production Server | `npm start` | Start production server | build |
| Node: Debug Server | `node --inspect server.js` | Start server in debug mode | build |
| Database: Run Migrations | `npx knex migrate:latest` | Run database migrations | build |
| Database: Rollback Migration | `npx knex migrate:rollback` | Rollback database migration | build |
| Database: Seed Data | `npx knex seed:run` | Seed database with test data | build |
| API: Generate Documentation | `npx swagger-jsdoc` | Generate API documentation | build |
| API: Test Endpoints | `npm run test:api` | Test API endpoints | test |
| Health: Check Server Status | `curl -f http://localhost:3000/health` | Check server health | test |
| PM2: Start Application | `npx pm2 start ecosystem.config.js` | Start with PM2 | build |
| PM2: Monitor Application | `npx pm2 monit` | Monitor PM2 processes | test |
| PM2: Restart Application | `npx pm2 restart all` | Restart PM2 processes | build |

#### React Development Tasks (`javascript/react.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| React: Start Development Server | `npm start` | Start React dev server | build |
| React: Build for Production | `npm run build` | Create production build | build |
| React: Analyze Bundle Size | `npx webpack-bundle-analyzer build/static/js/*.js` | Analyze bundle size | test |
| React: Generate Component | `npx generate-react-cli component` | Generate React component | build |
| Storybook: Start Server | `npm run storybook` | Start Storybook server | build |
| Storybook: Build Static | `npm run build-storybook` | Build static Storybook | build |
| Test: Component Tests | `npm test -- --watchAll=false` | Run component tests | test |
| Test: E2E with Cypress | `npx cypress run` | Run end-to-end tests | test |
| Test: Visual Regression | `npx chromatic` | Visual regression testing | test |
| Accessibility: Run axe Tests | `npx @axe-core/cli http://localhost:3000` | Accessibility testing | test |
| Performance: Lighthouse Audit | `npx lighthouse http://localhost:3000` | Performance audit | test |
| PWA: Generate Service Worker | `npx workbox generateSW` | Generate service worker | build |
| PWA: Validate Manifest | `npx web-app-manifest-validator` | Validate PWA manifest | test |
| Deployment: Deploy to Netlify | `npx netlify deploy --prod` | Deploy to Netlify | build |

### 🐳 Docker Development

#### General Docker Tasks (`docker/general.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| Docker: Build Image | `docker build -t ${workspaceFolderBasename}:latest .` | Build Docker image | build |
| Docker: Build Multi-stage Production | `docker build --target production` | Build production image | build |
| Docker: Run Container | `docker run -p 3000:3000` | Run container | build |
| Docker: Run Interactive Shell | `docker run -it --rm ${workspaceFolderBasename}:latest /bin/bash` | Interactive container shell | build |
| Docker: Debug Container | `docker run -p 3000:3000 -p 9229:9229` | Debug container | build |
| Docker: List Images | `docker images` | List Docker images | test |
| Docker: List Running Containers | `docker ps` | List running containers | test |
| Docker: Stop All Containers | `docker stop $(docker ps -q)` | Stop all containers | build |
| Docker: Clean Unused Resources | `docker system prune -f` | Clean unused resources | build |
| Docker: Security Scan with Trivy | `trivy image` | Security vulnerability scan | test |
| Docker: Vulnerability Scan with Snyk | `snyk container test` | Container security scan | test |
| Docker: Check Image Layers | `docker history` | Check image layer history | test |
| Docker: Optimize Image Size | `docker run --rm wagoodman/dive:latest` | Analyze image size | test |
| Docker: Tag for Registry | `docker tag` | Tag image for registry | build |
| Docker: Push to Registry | `docker push` | Push image to registry | build |

#### Docker Compose Tasks (`docker/compose.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| Compose: Start All Services | `docker-compose up -d` | Start all services | build |
| Compose: Start Development Environment | `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d` | Start dev environment | build |
| Compose: Start Production Environment | `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d` | Start prod environment | build |
| Compose: Build and Start | `docker-compose up --build -d` | Build and start services | build |
| Compose: Stop All Services | `docker-compose down` | Stop all services | build |
| Compose: Stop and Remove Volumes | `docker-compose down -v` | Stop and remove volumes | build |
| Compose: View Service Logs | `docker-compose logs -f` | View service logs | test |
| Compose: View Specific Service Logs | `docker-compose logs -f ${input:serviceName}` | View specific service logs | test |
| Compose: Check Service Status | `docker-compose ps` | Check service status | test |
| Compose: Execute Shell in Service | `docker-compose exec ${input:serviceName} /bin/bash` | Execute shell in service | build |
| Compose: Restart Service | `docker-compose restart ${input:serviceName}` | Restart specific service | build |
| Compose: Scale Service | `docker-compose up -d --scale ${input:serviceName}=${input:replicaCount}` | Scale service | build |
| Compose: Validate Configuration | `docker-compose config` | Validate compose config | test |
| Compose: Health Check | `docker-compose exec -T ${input:serviceName} curl -f http://localhost:${input:healthPort}/health` | Service health check | test |
| Compose: Database Backup | `docker-compose exec -T db pg_dump` | Backup database | build |

### 📊 Git Workflows

#### Git Workflow Tasks (`git/workflows.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| Git: Create Feature Branch | `git checkout -b feature/${input:featureName}` | Create feature branch | build |
| Git: Create Hotfix Branch | `git checkout -b hotfix/${input:hotfixName}` | Create hotfix branch | build |
| Git: Switch to Main Branch | `git checkout main` | Switch to main branch | build |
| Git: Update Main Branch | `git checkout main && git pull origin main` | Update main branch | build |
| Git: Merge Feature to Main | `git checkout main && git merge feature/${input:featureName} --no-ff` | Merge feature branch | build |
| Git: Interactive Rebase | `git rebase -i HEAD~${input:commitCount}` | Interactive rebase | build |
| Git: Squash Commits | `git reset --soft HEAD~${input:commitCount}` | Squash commits | build |
| Git: Check Repository Status | `git status --porcelain` | Check repository status | test |
| Git: Show Branch History | `git log --oneline --graph --decorate -10` | Show branch history | test |
| Git: Find Large Files | `git rev-list --objects --all` | Find large files in history | test |
| Git: Clean Merged Branches | `git branch --merged main \| grep -v main \| xargs -n 1 git branch -d` | Clean merged branches | build |
| Git: Validate Commit Messages | `commitizen check` | Validate commit messages | test |
| Git: Generate Changelog | `conventional-changelog -p angular -i CHANGELOG.md -s` | Generate changelog | build |
| Git: Create Release Tag | `git tag -a v${input:version} -m "Release version ${input:version}"` | Create release tag | build |
| Git: Push Tags | `git push origin --tags` | Push tags to remote | build |

#### Git Hooks Tasks (`git/hooks.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| Git Hooks: Install Pre-commit | `pre-commit install` | Install pre-commit hooks | build |
| Git Hooks: Run All Pre-commit Hooks | `pre-commit run --all-files` | Run all pre-commit hooks | test |
| Git Hooks: Update Hook Versions | `pre-commit autoupdate` | Update hook versions | build |
| Git Hooks: Validate Staged Files | `pre-commit run` | Validate staged files | test |
| Git Hooks: Lint Commit Message | `commitlint --edit .git/COMMIT_EDITMSG` | Lint commit message | test |
| Git Hooks: Run Tests Before Push | `npm test -- --watchAll=false --coverage` | Run tests before push | test |
| Git Hooks: Security Scan Before Commit | `git-secrets --scan` | Security scan before commit | test |
| Git Hooks: Install Git Secrets | `git-secrets --install` | Install git secrets | build |
| Git Hooks: Add AWS Secrets Patterns | `git-secrets --register-aws` | Add AWS secrets patterns | build |
| Git Hooks: Custom Pattern Check | `git-secrets --add ${input:secretPattern}` | Add custom secret pattern | build |
| Git Hooks: Install Husky | `npx husky install` | Install Husky hooks | build |
| Git Hooks: Add Pre-commit Hook | `npx husky add .husky/pre-commit "npm test"` | Add pre-commit hook | build |
| Git Hooks: Add Commit Message Hook | `npx husky add .husky/commit-msg "npx commitlint --edit $1"` | Add commit message hook | build |
| Git Hooks: Test Hook Configuration | `echo 'test commit' \| .husky/commit-msg` | Test hook configuration | test |

### 🔧 General Maintenance

#### Backup and Maintenance Tasks (`general/backup.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| Backup: Create Project Archive | `tar -czf ../backup_$(date +%Y%m%d_%H%M%S).tar.gz` | Create project backup | build |
| Backup: Git Repository Mirror | `git clone --mirror . ../mirror_$(date +%Y%m%d_%H%M%S).git` | Mirror git repository | build |
| Backup: Database Export | `pg_dump -h ${input:dbHost} -U ${input:dbUser} -d ${input:dbName}` | Export database | build |
| Cleanup: Remove Node Modules | `find . -name "node_modules" -type d -exec rm -rf {} +` | Remove node_modules | build |
| Cleanup: Remove Build Artifacts | `rm -rf build dist *.tgz coverage` | Remove build artifacts | build |
| Cleanup: Remove Log Files | `find . -name "*.log" -type f -delete` | Remove log files | build |
| Cleanup: Docker System Prune | `docker system prune -a -f` | Clean Docker system | build |
| Maintenance: Update Dependencies | `npm update` | Update dependencies | build |
| Maintenance: Check for Outdated Packages | `npm outdated` | Check outdated packages | test |
| Maintenance: Rebuild Package Lock | `rm package-lock.json && npm install` | Rebuild package lock | build |
| Maintenance: Git Garbage Collection | `git gc --aggressive --prune=now` | Git garbage collection | build |
| Maintenance: Verify Repository Integrity | `git fsck --full` | Verify repository integrity | test |
| Archive: Create Release Bundle | `npm run build && tar -czf release_v${input:version}.tar.gz build/` | Create release bundle | build |
| Archive: Generate Project Manifest | `find . -type f -not -path './.git/*' -not -path './node_modules/*'` | Generate project manifest | build |

#### Diagnostic Tasks (`general/diagnostics.json`)

| Task Name | Command | Description | Group |
|-----------|---------|-------------|-------|
| Diagnostics: System Information | `uname -a && free -h && df -h` | Show system information | test |
| Diagnostics: Node.js Environment | `node --version && npm --version && npm config list` | Check Node.js environment | test |
| Diagnostics: Python Environment | `python --version && pip --version && pip list` | Check Python environment | test |
| Diagnostics: Docker Environment | `docker --version && docker-compose --version && docker system df` | Check Docker environment | test |
| Diagnostics: Git Configuration | `git --version && git config --list && git status` | Check Git configuration | test |
| Diagnostics: Network Connectivity | `nslookup google.com && ping -c 3 google.com` | Check network connectivity | test |
| Diagnostics: Port Availability | `netstat -tuln` | Check port availability | test |
| Diagnostics: Running Processes | `ps aux \| grep -E "(node\|python\|docker)"` | Check running processes | test |
| Diagnostics: File Permissions Check | `find . -type f -not -perm 644` | Check file permissions | test |
| Diagnostics: Large Files Detection | `find . -type f -size +10M` | Find large files | test |
| Diagnostics: Performance Monitor | `top -n 1 -b` | Performance monitoring | test |
| Diagnostics: Dependency Tree | `npm ls --depth=2` | Show dependency tree | test |
| Diagnostics: Security Vulnerabilities | `npm audit --audit-level moderate` | Check security vulnerabilities | test |
| Diagnostics: Environment Variables | `env \| grep -E "(NODE\|NPM\|PATH\|HOME)"` | Show environment variables | test |
| Diagnostics: Generate Full Report | `echo 'Diagnostic Report' > diagnostic_report_$(date +%Y%m%d_%H%M%S).txt` | Generate diagnostic report | build |

## 🎯 Task Groups

Tasks are organized into the following VS Code task groups:

- **build**: Tasks that compile, package, or prepare the project
- **test**: Tasks that validate, check, or test the project
- **clean**: Tasks that clean up or reset the project state

## 🔧 Task Configuration

### Input Variables

Many tasks support input variables that are prompted when the task runs:

- `${input:featureName}`: Feature branch name
- `${input:version}`: Version number for releases
- `${input:serviceName}`: Docker service name
- `${input:commitCount}`: Number of commits for rebase/squash

### Workspace Variables

Tasks can use VS Code workspace variables:

- `${workspaceFolder}`: Current workspace folder path
- `${workspaceFolderBasename}`: Current workspace folder name
- `${file}`: Currently opened file
- `${relativeFile}`: Currently opened file relative to workspace

### Problem Matchers

Tasks include appropriate problem matchers for error detection:

- `$eslint-stylish`: ESLint error detection
- `$tsc`: TypeScript compiler errors
- `$jest`: Jest test failures
- `$python`: Python error detection

## 📋 Adding Custom Tasks

You can add custom tasks to your `.vscode/tasks.json` file following this structure:

```json
{
  "label": "My Custom Task",
  "type": "shell",
  "command": "echo",
  "args": ["Hello, World!"],
  "group": "build",
  "presentation": {
    "echo": true,
    "reveal": "always",
    "focus": false,
    "panel": "shared"
  }
}
```

## 🚀 Best Practices

1. **Use descriptive labels**: Make task names clear and descriptive
2. **Group tasks appropriately**: Use build, test, or clean groups
3. **Add problem matchers**: Include appropriate error detection
4. **Use input variables**: Make tasks reusable with input prompts
5. **Set working directories**: Ensure tasks run in the correct directory
6. **Handle errors gracefully**: Include error handling where appropriate

## 🔗 References

- [VS Code Tasks Documentation](https://code.visualstudio.com/docs/editor/tasks)
- [Task Schema Reference](https://json.schemastore.org/vscode-tasks)
- [Problem Matchers](https://code.visualstudio.com/docs/editor/tasks#_defining-a-problem-matcher)
