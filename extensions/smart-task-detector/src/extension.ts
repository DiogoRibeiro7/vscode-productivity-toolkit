import * as vscode from 'vscode';
import { ProjectDetector } from './services/ProjectDetector';
import { TaskInstaller } from './services/TaskInstaller';
import { TaskManager } from './services/TaskManager';
import { WelcomeProvider } from './providers/WelcomeProvider';
import { TasksTreeProvider } from './providers/TasksTreeProvider';
import { ProjectTreeProvider } from './providers/ProjectTreeProvider';
import { TaskManagerWebview } from './webviews/TaskManagerWebview';

export function activate(context: vscode.ExtensionContext) {
    vscode.window.showInformationMessage('Smart Task Detector extension is now active!');

    // Initialize services
    const projectDetector = new ProjectDetector();
    const taskInstaller = new TaskInstaller(context);
    const taskManager = new TaskManager(context, taskInstaller);
    
    // Initialize providers
    const tasksTreeProvider = new TasksTreeProvider(taskManager);
    const projectTreeProvider = new ProjectTreeProvider(projectDetector);
    const welcomeProvider = new WelcomeProvider(context);
    const taskManagerWebview = new TaskManagerWebview(context, taskManager);

    // Register tree views
    const tasksTreeView = vscode.window.createTreeView('smartTaskDetector.tasks', {
        treeDataProvider: tasksTreeProvider,
        showCollapseAll: true
    });

    const projectTreeView = vscode.window.createTreeView('smartTaskDetector.projects', {
        treeDataProvider: projectTreeProvider,
        showCollapseAll: true
    });

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('smartTaskDetector.detectAndInstall', async () => {
            await detectAndInstallTasks(projectDetector, taskManager, taskInstaller);
        }),

        vscode.commands.registerCommand('smartTaskDetector.openTaskManager', () => {
            taskManagerWebview.show();
        }),

        vscode.commands.registerCommand('smartTaskDetector.refreshTasks', () => {
            tasksTreeProvider.refresh();
            projectTreeProvider.refresh();
        }),

        vscode.commands.registerCommand('smartTaskDetector.installTask', async (taskItem) => {
            if (taskItem && taskItem.task) {
                await taskInstaller.installTask(taskItem.task);
                tasksTreeProvider.refresh();
                vscode.window.showInformationMessage(`Task "${taskItem.task.label}" installed successfully!`);
            }
        }),

        vscode.commands.registerCommand('smartTaskDetector.removeTask', async (taskItem) => {
            if (taskItem && taskItem.task) {
                await taskInstaller.removeTask(taskItem.task);
                tasksTreeProvider.refresh();
                vscode.window.showInformationMessage(`Task "${taskItem.task.label}" removed successfully!`);
            }
        }),

        vscode.commands.registerCommand('smartTaskDetector.showWelcome', () => {
            welcomeProvider.show();
        })
    );

    // Auto-detect on workspace open
    const config = vscode.workspace.getConfiguration('smartTaskDetector');
    if (config.get('autoDetect', true)) {
        detectAndInstallTasks(projectDetector, taskManager, taskInstaller);
    }

    // Show welcome on first run
    if (config.get('showWelcomeOnFirstRun', true)) {
        const hasShownWelcome = context.globalState.get('hasShownWelcome', false);
        if (!hasShownWelcome) {
            welcomeProvider.show();
            context.globalState.update('hasShownWelcome', true);
        }
    }

    // Register event handlers
    vscode.workspace.onDidChangeWorkspaceFolders(() => {
        projectTreeProvider.refresh();
        if (config.get('autoDetect', true)) {
            detectAndInstallTasks(projectDetector, taskManager, taskInstaller);
        }
    });

    // Store references for testing
    context.subscriptions.push(tasksTreeView, projectTreeView);
}

async function detectAndInstallTasks(
    projectDetector: ProjectDetector,
    taskManager: TaskManager,
    taskInstaller: TaskInstaller
) {
    try {
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Detecting project types and suggesting tasks...",
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0 });

            // Detect project types
            const detectedProjects = await projectDetector.detectProjectTypes();
            progress.report({ increment: 50, message: "Analyzing project structure..." });

            if (detectedProjects.length === 0) {
                vscode.window.showInformationMessage("No recognized project types found in workspace.");
                return;
            }

            // Get available tasks for detected projects
            const availableTasks = await taskManager.getAvailableTasksForProjects(detectedProjects);
            progress.report({ increment: 80, message: "Loading task suggestions..." });

            if (availableTasks.length === 0) {
                vscode.window.showInformationMessage("No tasks available for detected project types.");
                return;
            }

            progress.report({ increment: 100, message: "Complete!" });

            // Show suggestions to user
            const projectTypes = detectedProjects.map(p => p.type).join(', ');
            const choice = await vscode.window.showInformationMessage(
                `Detected ${detectedProjects.length} project type(s): ${projectTypes}. Would you like to install recommended tasks?`,
                { modal: false },
                'Install All',
                'Choose Tasks',
                'Skip'
            );

            if (choice === 'Install All') {
                await taskInstaller.installMultipleTasks(availableTasks);
                vscode.window.showInformationMessage(`Successfully installed ${availableTasks.length} tasks!`);
            } else if (choice === 'Choose Tasks') {
                // Open task manager for manual selection
                vscode.commands.executeCommand('smartTaskDetector.openTaskManager');
            }
        });

    } catch (error) {
        vscode.window.showErrorMessage(`Error detecting and installing tasks: ${error instanceof Error ? error.message : String(error)}`);
    }
}

export function deactivate() {
export function deactivate() {
    vscode.window.showInformationMessage('Smart Task Detector extension is now deactivated.');
}
