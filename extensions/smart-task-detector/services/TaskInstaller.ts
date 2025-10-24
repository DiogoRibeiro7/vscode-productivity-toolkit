import * as vscode from 'vscode';
import * as fs from 'fs-extra';
import * as path from 'path';

export interface Task {
    label: string;
    type: string;
    command: string;
    args?: string[];
    group?: string | { kind: string; isDefault?: boolean };
    presentation?: {
        echo?: boolean;
        reveal?: string;
        focus?: boolean;
        panel?: string;
    };
    problemMatcher?: string | string[];
    isBackground?: boolean;
}

export interface TaskCategory {
    taskVersion: string;
    category: string;
    displayName: string;
    description: string;
    tasks: Task[];
}

export class TaskInstaller {
    private context: vscode.ExtensionContext;
    private readonly tasksFilePath: string;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            throw new Error('No workspace folder found');
        }
        this.tasksFilePath = path.join(workspaceFolder.uri.fsPath, '.vscode', 'tasks.json');
    }

    async installTask(task: Task): Promise<void> {
        try {
            await this.ensureVSCodeFolder();
            const currentTasks = await this.readCurrentTasks();
            
            // Check if task already exists
            const existingTaskIndex = currentTasks.tasks.findIndex(t => t.label === task.label);
            
            if (existingTaskIndex >= 0) {
                // Update existing task
                currentTasks.tasks[existingTaskIndex] = task;
                vscode.window.showInformationMessage(`Task "${task.label}" updated successfully!`);
            } else {
                // Add new task
                currentTasks.tasks.push(task);
                vscode.window.showInformationMessage(`Task "${task.label}" installed successfully!`);
            }

            await this.writeTasksFile(currentTasks);
            
        } catch (error) {
            console.error('Error installing task:', error);
            vscode.window.showErrorMessage(`Failed to install task: ${error instanceof Error ? error.message : String(error)}`);
        }
    }

    async installMultipleTasks(tasks: Task[]): Promise<void> {
        try {
            await this.ensureVSCodeFolder();
            const currentTasks = await this.readCurrentTasks();
            
            let installedCount = 0;
            let updatedCount = 0;

            for (const task of tasks) {
                const existingTaskIndex = currentTasks.tasks.findIndex(t => t.label === task.label);
                
                if (existingTaskIndex >= 0) {
                    currentTasks.tasks[existingTaskIndex] = task;
                    updatedCount++;
                } else {
                    currentTasks.tasks.push(task);
                    installedCount++;
                }
            }

            await this.writeTasksFile(currentTasks);
            
            const message = `Successfully processed ${tasks.length} tasks: ${installedCount} installed, ${updatedCount} updated.`;
            vscode.window.showInformationMessage(message);
            
        } catch (error) {
            console.error('Error installing multiple tasks:', error);
            vscode.window.showErrorMessage(`Failed to install tasks: ${error instanceof Error ? error.message : String(error)}`);
        }
    }

    async removeTask(task: Task): Promise<void> {
        try {
            const currentTasks = await this.readCurrentTasks();
            const initialLength = currentTasks.tasks.length;
            
            currentTasks.tasks = currentTasks.tasks.filter(t => t.label !== task.label);
            
            if (currentTasks.tasks.length < initialLength) {
                await this.writeTasksFile(currentTasks);
                vscode.window.showInformationMessage(`Task "${task.label}" removed successfully!`);
            } else {
                vscode.window.showWarningMessage(`Task "${task.label}" not found.`);
            }
            
        } catch (error) {
            console.error('Error removing task:', error);
            vscode.window.showErrorMessage(`Failed to remove task: ${error instanceof Error ? error.message : String(error)}`);
        }
    }

    async getInstalledTasks(): Promise<Task[]> {
        try {
            const tasksConfig = await this.readCurrentTasks();
            return tasksConfig.tasks || [];
        } catch (error) {
            console.error('Error reading installed tasks:', error);
            return [];
        }
    }

    async installTaskCategory(category: TaskCategory): Promise<void> {
        const config = vscode.workspace.getConfiguration('smartTaskDetector');
        const enableNotifications = config.get('enableNotifications', true);

        try {
            await this.installMultipleTasks(category.tasks);
            
            if (enableNotifications) {
                vscode.window.showInformationMessage(
                    `Installed ${category.tasks.length} tasks from "${category.displayName}" category.`
                );
            }
            
        } catch (error) {
            console.error(`Error installing task category ${category.category}:`, error);
            vscode.window.showErrorMessage(`Failed to install category: ${error instanceof Error ? error.message : String(error)}`);
        }
    }

    private async ensureVSCodeFolder(): Promise<void> {
        const vscodeFolder = path.dirname(this.tasksFilePath);
        await fs.ensureDir(vscodeFolder);
    }

    private async readCurrentTasks(): Promise<{ version: string; tasks: Task[] }> {
        try {
            if (await fs.pathExists(this.tasksFilePath)) {
                const content = await fs.readFile(this.tasksFilePath, 'utf8');
                const parsed = JSON.parse(content);
                
                return {
                    version: parsed.version || '2.0.0',
                    tasks: parsed.tasks || []
                };
            }
        } catch (error) {
            console.error('Error reading tasks.json:', error);
        }

        // Return default structure if file doesn't exist or is invalid
        return {
            version: '2.0.0',
            tasks: []
        };
    }

    private async writeTasksFile(tasksConfig: { version: string; tasks: Task[] }): Promise<void> {
        const content = JSON.stringify(tasksConfig, null, 4);
        await fs.writeFile(this.tasksFilePath, content, 'utf8');
    }

    async createBackup(): Promise<string> {
        try {
            if (!await fs.pathExists(this.tasksFilePath)) {
                throw new Error('No tasks.json file to backup');
            }

            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const backupPath = this.tasksFilePath.replace('.json', `_backup_${timestamp}.json`);
            
            await fs.copy(this.tasksFilePath, backupPath);
            return backupPath;
            
        } catch (error) {
            console.error('Error creating backup:', error);
            throw error;
        }
    }

    async restoreFromBackup(backupPath: string): Promise<void> {
        try {
            if (!await fs.pathExists(backupPath)) {
                throw new Error('Backup file not found');
            }

            await fs.copy(backupPath, this.tasksFilePath);
            vscode.window.showInformationMessage('Tasks restored from backup successfully!');
            
        } catch (error) {
            console.error('Error restoring from backup:', error);
            vscode.window.showErrorMessage(`Failed to restore backup: ${error instanceof Error ? error.message : String(error)}`);
            throw error;
        }
    }
}
