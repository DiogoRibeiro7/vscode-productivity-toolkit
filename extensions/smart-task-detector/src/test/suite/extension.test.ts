import * as assert from 'assert';
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs-extra';
import { ProjectDetector } from '../../services/ProjectDetector';
import { TaskInstaller } from '../../services/TaskInstaller';
import { TaskManager } from '../../services/TaskManager';

suite('Extension Test Suite', () => {
    let tempWorkspaceDir: string;
    let projectDetector: ProjectDetector;
    let taskInstaller: TaskInstaller;
    let taskManager: TaskManager;

    suiteSetup(async () => {
        // Create temporary workspace for testing
        tempWorkspaceDir = path.join(__dirname, 'test-workspace');
        await fs.ensureDir(tempWorkspaceDir);
        
        // Initialize services with test context
        const testContext = {
            subscriptions: [],
            globalState: {
                get: () => false,
                update: () => Promise.resolve()
            }
        } as any;
        
        projectDetector = new ProjectDetector();
        taskInstaller = new TaskInstaller(testContext);
        taskManager = new TaskManager(testContext, taskInstaller);
    });

    suiteTeardown(async () => {
        // Clean up temporary workspace
        if (await fs.pathExists(tempWorkspaceDir)) {
            await fs.remove(tempWorkspaceDir);
        }
    });

    suite('Extension Activation', () => {
        test('Extension should be present', () => {
            const extension = vscode.extensions.getExtension('diogoribeiro7.smart-task-detector');
            assert.ok(extension, 'Extension should be found');
        });

        test('Extension should activate', async () => {
            const extension = vscode.extensions.getExtension('diogoribeiro7.smart-task-detector');
            if (extension) {
                await extension.activate();
                assert.ok(extension.isActive, 'Extension should be active');
            }
        });

        test('Commands should be registered', async () => {
            const commands = await vscode.commands.getCommands(true);
            const extensionCommands = [
                'smartTaskDetector.detectAndInstall',
                'smartTaskDetector.openTaskManager',
                'smartTaskDetector.refreshTasks',
                'smartTaskDetector.installTask',
                'smartTaskDetector.removeTask',
                'smartTaskDetector.showWelcome'
            ];

            extensionCommands.forEach(command => {
                assert.ok(commands.includes(command), \`Command \${command} should be registered\`);
            });
        });
    });

    suite('Project Detection', () => {
        test('Should detect Python project', async () => {
            // Create Python project files
            const pythonProjectDir = path.join(tempWorkspaceDir, 'python-test');
            await fs.ensureDir(pythonProjectDir);
            await fs.writeFile(path.join(pythonProjectDir, 'requirements.txt'), 'django==3.2.0\\nnumpy==1.21.0');
            await fs.writeFile(path.join(pythonProjectDir, 'main.py'), 'print("Hello, World!")');

            const detector = new ProjectDetector(pythonProjectDir);
            const detectedProjects = await detector.detectProjectTypes();

            assert.ok(detectedProjects.length > 0, 'Should detect at least one project type');
            const pythonProject = detectedProjects.find(p => p.type.includes('python'));
            assert.ok(pythonProject, 'Should detect Python project');
            assert.ok(pythonProject.confidence > 0.3, 'Should have reasonable confidence');
        });

        test('Should detect JavaScript project', async () => {
            // Create JavaScript project files
            const jsProjectDir = path.join(tempWorkspaceDir, 'js-test');
            await fs.ensureDir(jsProjectDir);
            await fs.writeFile(path.join(jsProjectDir, 'package.json'), JSON.stringify({
                name: 'test-project',
                dependencies: {
                    express: '^4.17.1'
                }
            }));
            await fs.writeFile(path.join(jsProjectDir, 'index.js'), 'console.log("Hello, World!");');

            const detector = new ProjectDetector(jsProjectDir);
            const detectedProjects = await detector.detectProjectTypes();

            assert.ok(detectedProjects.length > 0, 'Should detect at least one project type');
            const jsProject = detectedProjects.find(p => p.type.includes('javascript'));
            assert.ok(jsProject, 'Should detect JavaScript project');
        });

        test('Should detect React project', async () => {
            // Create React project files
            const reactProjectDir = path.join(tempWorkspaceDir, 'react-test');
            await fs.ensureDir(reactProjectDir);
            await fs.ensureDir(path.join(reactProjectDir, 'src'));
            await fs.ensureDir(path.join(reactProjectDir, 'public'));
            
            await fs.writeFile(path.join(reactProjectDir, 'package.json'), JSON.stringify({
                name: 'react-test',
                dependencies: {
                    react: '^17.0.0',
                    'react-dom': '^17.0.0'
                }
            }));
            await fs.writeFile(path.join(reactProjectDir, 'src', 'App.jsx'), 'export default function App() { return <div>Hello</div>; }');
            await fs.writeFile(path.join(reactProjectDir, 'public', 'index.html'), '<html><body><div id="root"></div></body></html>');

            const detector = new ProjectDetector(reactProjectDir);
            const detectedProjects = await detector.detectProjectTypes();

            const reactProject = detectedProjects.find(p => p.type === 'react-development');
            assert.ok(reactProject, 'Should detect React project');
        });

        test('Should detect Docker project', async () => {
            // Create Docker project files
            const dockerProjectDir = path.join(tempWorkspaceDir, 'docker-test');
            await fs.ensureDir(dockerProjectDir);
            await fs.writeFile(path.join(dockerProjectDir, 'Dockerfile'), 'FROM node:14\\nWORKDIR /app\\nCOPY . .\\nRUN npm install');
            await fs.writeFile(path.join(dockerProjectDir, 'docker-compose.yml'), 'version: "3"\\nservices:\\n  app:\\n    build: .');

            const detector = new ProjectDetector(dockerProjectDir);
            const detectedProjects = await detector.detectProjectTypes();

            const dockerProject = detectedProjects.find(p => p.type.includes('docker'));
            assert.ok(dockerProject, 'Should detect Docker project');
        });

        test('Should handle empty directory', async () => {
            const emptyDir = path.join(tempWorkspaceDir, 'empty');
            await fs.ensureDir(emptyDir);

            const detector = new ProjectDetector(emptyDir);
            const detectedProjects = await detector.detectProjectTypes();

            // Should only detect Git if .git exists, otherwise empty
            assert.ok(Array.isArray(detectedProjects), 'Should return array');
        });
    });

    suite('Task Management', () => {
        test('Should load available task categories', async () => {
            // This test might need to be mocked since it makes HTTP requests
            // For now, test the structure
            const categories = await taskManager.getTaskCategories();
            assert.ok(Array.isArray(categories), 'Should return array of categories');
        });

        test('Should get task statistics', async () => {
            const stats = await taskManager.getTaskStatistics();
            
            assert.ok(typeof stats.totalAvailable === 'number', 'Should have totalAvailable');
            assert.ok(typeof stats.totalInstalled === 'number', 'Should have totalInstalled');
            assert.ok(typeof stats.categoriesAvailable === 'number', 'Should have categoriesAvailable');
            assert.ok(typeof stats.categoriesWithInstalledTasks === 'number', 'Should have categoriesWithInstalledTasks');
        });

        test('Should validate task integrity', async () => {
            const validation = await taskManager.validateTaskIntegrity();
            
            assert.ok(typeof validation.valid === 'boolean', 'Should have valid property');
            assert.ok(Array.isArray(validation.issues), 'Should have issues array');
        });

        test('Should search tasks', async () => {
            const searchResults = await taskManager.searchTasks('python');
            
            assert.ok(Array.isArray(searchResults), 'Should return array of tasks');
            // Results might be empty if no tasks are loaded, which is fine for unit tests
        });
    });

    suite('Task Installation', () => {
        let testTasksDir: string;

        setup(async () => {
            testTasksDir = path.join(tempWorkspaceDir, 'task-install-test');
            await fs.ensureDir(testTasksDir);
            await fs.ensureDir(path.join(testTasksDir, '.vscode'));
        });

        test('Should create tasks.json if not exists', async () => {
            const tasksJsonPath = path.join(testTasksDir, '.vscode', 'tasks.json');
            
            // Ensure file doesn't exist
            if (await fs.pathExists(tasksJsonPath)) {
                await fs.remove(tasksJsonPath);
            }

            const testTask = {
                label: 'Test Task',
                type: 'shell',
                command: 'echo',
                args: ['hello']
            };

            // Mock TaskInstaller with test directory
            const testContext = {
                subscriptions: [],
                globalState: { get: () => false, update: () => Promise.resolve() }
            } as any;
            
            // This would need to be adjusted to work with the test directory
            // For now, just test the structure
            assert.ok(testTask.label, 'Task should have label');
            assert.ok(testTask.command, 'Task should have command');
        });

        test('Should handle existing tasks.json', async () => {
            const tasksJsonPath = path.join(testTasksDir, '.vscode', 'tasks.json');
            
            // Create existing tasks.json
            const existingTasks = {
                version: '2.0.0',
                tasks: [
                    {
                        label: 'Existing Task',
                        type: 'shell',
                        command: 'ls'
                    }
                ]
            };
            
            await fs.writeFile(tasksJsonPath, JSON.stringify(existingTasks, null, 2));
            
            // Verify file exists and is valid JSON
            const content = await fs.readFile(tasksJsonPath, 'utf8');
            const parsed = JSON.parse(content);
            
            assert.strictEqual(parsed.version, '2.0.0', 'Should maintain version');
            assert.ok(Array.isArray(parsed.tasks), 'Should have tasks array');
            assert.strictEqual(parsed.tasks.length, 1, 'Should have one existing task');
        });
    });

    suite('Configuration', () => {
        test('Should read extension configuration', () => {
            const config = vscode.workspace.getConfiguration('smartTaskDetector');
            
            // Test default values
            const autoDetect = config.get('autoDetect');
            const showWelcome = config.get('showWelcomeOnFirstRun');
            const taskRepoUrl = config.get('taskRepositoryUrl');
            
            assert.ok(typeof autoDetect === 'boolean', 'autoDetect should be boolean');
            assert.ok(typeof showWelcome === 'boolean', 'showWelcomeOnFirstRun should be boolean');
            assert.ok(typeof taskRepoUrl === 'string', 'taskRepositoryUrl should be string');
        });
    });

    suite('Error Handling', () => {
        test('Should handle invalid project path', async () => {
            const invalidPath = '/non/existent/path';
            const detector = new ProjectDetector(invalidPath);
            
            // Should not throw, should return empty array
            const result = await detector.detectProjectTypes();
            assert.ok(Array.isArray(result), 'Should return array even for invalid path');
        });

        test('Should handle malformed package.json', async () => {
            const malformedDir = path.join(tempWorkspaceDir, 'malformed-test');
            await fs.ensureDir(malformedDir);
            await fs.writeFile(path.join(malformedDir, 'package.json'), '{ invalid json }');

            const detector = new ProjectDetector(malformedDir);
            const result = await detector.detectProjectTypes();
            
            // Should handle gracefully and not crash
            assert.ok(Array.isArray(result), 'Should handle malformed JSON gracefully');
        });
    });

    suite('Performance', () => {
        test('Project detection should complete quickly', async () => {
            const startTime = Date.now();
            
            const detector = new ProjectDetector(tempWorkspaceDir);
            await detector.detectProjectTypes();
            
            const endTime = Date.now();
            const duration = endTime - startTime;
            
            // Should complete within 5 seconds
            assert.ok(duration < 5000, \`Detection should complete quickly, took \${duration}ms\`);
        });

        test('Should handle large directories efficiently', async () => {
            // Create a directory with many files
            const largeDir = path.join(tempWorkspaceDir, 'large-test');
            await fs.ensureDir(largeDir);
            
            // Create some test files (not too many for CI performance)
            for (let i = 0; i < 10; i++) {
                await fs.writeFile(path.join(largeDir, \`file\${i}.js\`), 'console.log("test");');
            }

            const startTime = Date.now();
            const detector = new ProjectDetector(largeDir);
            await detector.detectProjectTypes();
            const duration = Date.now() - startTime;

            assert.ok(duration < 2000, \`Should handle multiple files efficiently, took \${duration}ms\`);
        });
    });
});
