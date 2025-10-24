import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export interface DetectedProject {
    type: string;
    confidence: number;
    indicators: string[];
    rootPath: string;
}

export class ProjectDetector {
    private readonly detectionRules: DetectionRule[] = [
        // Python projects
        {
            type: 'python-general',
            patterns: ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', '*.py'],
            weights: { 'requirements.txt': 0.9, 'setup.py': 0.8, 'pyproject.toml': 0.9, 'Pipfile': 0.8, '*.py': 0.3 }
        },
        {
            type: 'python-data-science',
            patterns: ['*.ipynb', 'environment.yml', 'conda.yml'],
            dependencies: ['pandas', 'numpy', 'matplotlib', 'jupyter', 'scikit-learn'],
            weights: { '*.ipynb': 0.9, 'environment.yml': 0.8, 'conda.yml': 0.8 }
        },
        
        // JavaScript/Node.js projects
        {
            type: 'javascript-general',
            patterns: ['package.json', '*.js', '*.ts', 'tsconfig.json'],
            weights: { 'package.json': 0.9, 'tsconfig.json': 0.8, '*.js': 0.3, '*.ts': 0.4 }
        },
        {
            type: 'node-server',
            patterns: ['server.js', 'app.js', 'index.js'],
            dependencies: ['express', 'fastify', 'koa', 'hapi'],
            weights: { 'server.js': 0.9, 'app.js': 0.7, 'index.js': 0.5 }
        },
        {
            type: 'react-development',
            patterns: ['src/App.jsx', 'src/App.tsx', 'public/index.html'],
            dependencies: ['react', 'react-dom', '@types/react'],
            weights: { 'src/App.jsx': 0.9, 'src/App.tsx': 0.9, 'public/index.html': 0.6 }
        },
        
        // Docker projects
        {
            type: 'docker-general',
            patterns: ['Dockerfile', '.dockerignore'],
            weights: { 'Dockerfile': 0.9, '.dockerignore': 0.7 }
        },
        {
            type: 'docker-compose',
            patterns: ['docker-compose.yml', 'docker-compose.yaml', 'docker-compose.*.yml'],
            weights: { 'docker-compose.yml': 0.9, 'docker-compose.yaml': 0.9, 'docker-compose.*.yml': 0.8 }
        },
        
        // Git projects
        {
            type: 'git-workflows',
            patterns: ['.git', '.gitignore', '.github'],
            weights: { '.git': 0.9, '.gitignore': 0.7, '.github': 0.8 }
        }
    ];

    async detectProjectTypes(): Promise<DetectedProject[]> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            return [];
        }

        const detectedProjects: DetectedProject[] = [];

        for (const folder of workspaceFolders) {
            const folderPath = folder.uri.fsPath;
            const projectDetections = await this.analyzeFolder(folderPath);
            detectedProjects.push(...projectDetections);
        }

        // Sort by confidence and remove duplicates
        return detectedProjects
            .filter(project => project.confidence >= 0.3)
            .sort((a, b) => b.confidence - a.confidence)
            .filter((project, index, array) => 
                array.findIndex(p => p.type === project.type) === index
            );
    }

    private async analyzeFolder(folderPath: string): Promise<DetectedProject[]> {
        const detections: DetectedProject[] = [];

        for (const rule of this.detectionRules) {
            const detection = await this.evaluateRule(rule, folderPath);
            if (detection) {
                detections.push(detection);
            }
        }

        return detections;
    }

    private async evaluateRule(rule: DetectionRule, folderPath: string): Promise<DetectedProject | null> {
        let totalScore = 0;
        let maxScore = 0;
        const foundIndicators: string[] = [];

        // Check file patterns
        for (const pattern of rule.patterns) {
            const weight = rule.weights[pattern] || 0.5;
            maxScore += weight;

            if (await this.patternExists(pattern, folderPath)) {
                totalScore += weight;
                foundIndicators.push(pattern);
            }
        }

        // Check dependencies if pattern includes package.json
        if (rule.dependencies && foundIndicators.includes('package.json')) {
            const packageJsonPath = path.join(folderPath, 'package.json');
            const depScore = await this.checkDependencies(packageJsonPath, rule.dependencies);
            totalScore += depScore;
            maxScore += 1;
            
            if (depScore > 0.3) {
                foundIndicators.push(`dependencies: ${rule.dependencies.join(', ')}`);
            }
        }

        // Check dependencies if pattern includes requirements.txt or setup.py
        if (rule.dependencies && (foundIndicators.includes('requirements.txt') || foundIndicators.includes('setup.py'))) {
            const depScore = await this.checkPythonDependencies(folderPath, rule.dependencies);
            totalScore += depScore;
            maxScore += 1;
            
            if (depScore > 0.3) {
                foundIndicators.push(`python dependencies: ${rule.dependencies.join(', ')}`);
            }
        }

        const confidence = maxScore > 0 ? totalScore / maxScore : 0;

        if (confidence >= 0.3 && foundIndicators.length > 0) {
            return {
                type: rule.type,
                confidence,
                indicators: foundIndicators,
                rootPath: folderPath
            };
        }

        return null;
    }

    private async patternExists(pattern: string, folderPath: string): Promise<boolean> {
        try {
            if (pattern.includes('*')) {
                // Handle glob patterns
                const files = await this.findFiles(folderPath, pattern);
                return files.length > 0;
            } else {
                // Handle exact file/folder names
                const fullPath = path.join(folderPath, pattern);
                return fs.existsSync(fullPath);
            }
        } catch (error) {
            console.error(`Error checking pattern ${pattern}:`, error);
            return false;
        }
    }

    private async findFiles(folderPath: string, pattern: string): Promise<string[]> {
        // Simple glob implementation for common patterns
        const files: string[] = [];
        
        try {
            const entries = fs.readdirSync(folderPath, { withFileTypes: true });
            
            for (const entry of entries) {
                if (entry.isFile()) {
                    if (this.matchesPattern(entry.name, pattern)) {
                        files.push(entry.name);
                    }
                } else if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
                    // Recursively search subdirectories for specific patterns
                    const subPath = path.join(folderPath, entry.name);
                    const subFiles = await this.findFiles(subPath, pattern);
                    files.push(...subFiles.map(f => path.join(entry.name, f)));
                }
            }
        } catch (error) {
            console.error(`Error reading directory ${folderPath}:`, error);
        }

        return files;
    }

    private matchesPattern(filename: string, pattern: string): boolean {
        // Convert simple glob pattern to regex
        const regexPattern = pattern
            .replace(/\./g, '\\.')
            .replace(/\*/g, '.*');
        
        const regex = new RegExp(`^${regexPattern}$`);
        return regex.test(filename);
    }

    private async checkDependencies(packageJsonPath: string, dependencies: string[]): Promise<number> {
        try {
            if (!fs.existsSync(packageJsonPath)) {
                return 0;
            }

            const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
            const allDeps = {
                ...packageJson.dependencies,
                ...packageJson.devDependencies,
                ...packageJson.peerDependencies
            };

            const foundDeps = dependencies.filter(dep => dep in allDeps);
            return foundDeps.length / dependencies.length;
        } catch (error) {
            console.error(`Error checking dependencies in ${packageJsonPath}:`, error);
            return 0;
        }
    }

    private async checkPythonDependencies(folderPath: string, dependencies: string[]): Promise<number> {
        try {
            const requirementsPath = path.join(folderPath, 'requirements.txt');
            let content = '';

            if (fs.existsSync(requirementsPath)) {
                content += fs.readFileSync(requirementsPath, 'utf8');
            }

            const setupPyPath = path.join(folderPath, 'setup.py');
            if (fs.existsSync(setupPyPath)) {
                content += fs.readFileSync(setupPyPath, 'utf8');
            }

            const foundDeps = dependencies.filter(dep => 
                content.toLowerCase().includes(dep.toLowerCase())
            );
            
            return foundDeps.length / dependencies.length;
        } catch (error) {
            console.error(`Error checking Python dependencies in ${folderPath}:`, error);
            return 0;
        }
    }
}

interface DetectionRule {
    type: string;
    patterns: string[];
    dependencies?: string[];
    weights: { [pattern: string]: number };
}
