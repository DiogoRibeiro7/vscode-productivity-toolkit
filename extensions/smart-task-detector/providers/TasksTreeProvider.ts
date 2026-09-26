import * as vscode from 'vscode';

import { AvailableTask, TaskManager } from '../services/TaskManager';

export class TaskTreeItem extends vscode.TreeItem {
    constructor(public readonly task: AvailableTask) {
        super(task.label, vscode.TreeItemCollapsibleState.None);
        this.description = task.category;
        this.contextValue = task.isInstalled ? 'installedTask' : 'availableTask';
        this.iconPath = new vscode.ThemeIcon(task.isInstalled ? 'check' : 'add');
    }
}

export class TasksTreeProvider implements vscode.TreeDataProvider<TaskTreeItem> {
    private readonly emitter = new vscode.EventEmitter<TaskTreeItem | undefined | void>();
    readonly onDidChangeTreeData = this.emitter.event;

    constructor(private readonly taskManager: TaskManager) {}

    refresh(): void {
        this.emitter.fire();
    }

    getTreeItem(element: TaskTreeItem): vscode.TreeItem {
        return element;
    }

    async getChildren(): Promise<TaskTreeItem[]> {
        const tasks = await this.taskManager.getAllAvailableTasks();
        return tasks.map(task => new TaskTreeItem(task));
    }
}
