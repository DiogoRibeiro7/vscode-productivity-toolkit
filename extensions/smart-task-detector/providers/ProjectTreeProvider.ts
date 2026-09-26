import * as vscode from 'vscode';

import { DetectedProject, ProjectDetector } from '../services/ProjectDetector';

export class ProjectTreeItem extends vscode.TreeItem {
    constructor(project: DetectedProject) {
        super(project.type, vscode.TreeItemCollapsibleState.None);
        this.description = `${Math.round(project.confidence * 100)}%`;
        this.tooltip = project.indicators.join(', ');
        this.iconPath = new vscode.ThemeIcon('project');
    }
}

export class ProjectTreeProvider implements vscode.TreeDataProvider<ProjectTreeItem> {
    private readonly emitter = new vscode.EventEmitter<ProjectTreeItem | undefined | void>();
    readonly onDidChangeTreeData = this.emitter.event;

    constructor(private readonly detector: ProjectDetector) {}

    refresh(): void {
        this.emitter.fire();
    }

    getTreeItem(element: ProjectTreeItem): vscode.TreeItem {
        return element;
    }

    async getChildren(): Promise<ProjectTreeItem[]> {
        const projects = await this.detector.detectProjectTypes();
        return projects.map(project => new ProjectTreeItem(project));
    }
}
