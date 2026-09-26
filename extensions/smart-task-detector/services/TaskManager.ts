import * as https from 'https';
import * as vscode from 'vscode';

import { DetectedProject } from './ProjectDetector';
import { Task, TaskCategory, TaskInstaller } from './TaskInstaller';

export interface AvailableTask extends Task {
    category: string;
    isInstalled: boolean;
}

export interface TaskStatistics {
    totalAvailable: number;
    totalInstalled: number;
    categoriesAvailable: number;
    categoriesWithInstalledTasks: number;
}

const CATEGORY_PATHS: Record<string, string> = {
    'python-general': 'python/general.json',
    'python-data-science': 'python/data-science.json',
    'javascript-general': 'javascript/general.json',
    'react-development': 'javascript/react.json',
    'javascript-node': 'javascript/node.json',
    'node-server': 'javascript/node.json',
    'docker-general': 'docker/general.json',
    'docker-compose': 'docker/compose.json',
    'git-workflows': 'git/workflows.json'
};

export class TaskManager {
    private readonly categories = new Map<string, TaskCategory>();

    constructor(
        private readonly context: vscode.ExtensionContext,
        public readonly taskInstaller: TaskInstaller
    ) {}

    async getTaskCategories(): Promise<TaskCategory[]> {
        const categories = await Promise.all(
            Object.keys(CATEGORY_PATHS).map(category => this.loadCategory(category))
        );
        return categories.filter((category): category is TaskCategory => category !== null);
    }

    async getAllAvailableTasks(): Promise<AvailableTask[]> {
        const [categories, installed] = await Promise.all([
            this.getTaskCategories(),
            this.taskInstaller.getInstalledTasks()
        ]);
        const installedLabels = new Set(installed.map(task => task.label));

        return categories.flatMap(category =>
            category.tasks.map(task => ({
                ...task,
                category: category.category,
                isInstalled: installedLabels.has(task.label)
            }))
        );
    }

    async getAvailableTasksForProjects(projects: DetectedProject[]): Promise<AvailableTask[]> {
        const wanted = new Set(projects.map(project => this.normaliseCategory(project.type)));
        const tasks = await this.getAllAvailableTasks();
        return tasks.filter(task => wanted.has(task.category) && !task.isInstalled);
    }

    async getTaskStatistics(): Promise<TaskStatistics> {
        const [tasks, categories] = await Promise.all([
            this.getAllAvailableTasks(),
            this.getTaskCategories()
        ]);
        const installed = tasks.filter(task => task.isInstalled);
        const installedCategories = new Set(installed.map(task => task.category));

        return {
            totalAvailable: tasks.length,
            totalInstalled: installed.length,
            categoriesAvailable: categories.length,
            categoriesWithInstalledTasks: installedCategories.size
        };
    }

    async searchTasks(query: string): Promise<AvailableTask[]> {
        const needle = query.trim().toLowerCase();
        if (!needle) {
            return this.getAllAvailableTasks();
        }
        const tasks = await this.getAllAvailableTasks();
        return tasks.filter(task =>
            task.label.toLowerCase().includes(needle) ||
            task.category.toLowerCase().includes(needle) ||
            task.command.toLowerCase().includes(needle)
        );
    }

    async installTasksByCategory(categoryName: string): Promise<void> {
        const category = await this.loadCategory(this.normaliseCategory(categoryName));
        if (!category) {
            throw new Error(`Unknown task category: ${categoryName}`);
        }
        await this.taskInstaller.installTaskCategory(category);
    }

    async exportTasks(): Promise<string> {
        const installed = await this.taskInstaller.getInstalledTasks();
        return JSON.stringify({ version: '2.0.0', tasks: installed }, null, 2);
    }

    async importTasks(payload: string): Promise<void> {
        const parsed: unknown = JSON.parse(payload);
        if (!this.isTaskExport(parsed)) {
            throw new Error('Invalid task export format');
        }
        await this.taskInstaller.installMultipleTasks(parsed.tasks);
    }

    async validateTaskIntegrity(): Promise<{ valid: boolean; issues: string[] }> {
        const tasks = await this.getAllAvailableTasks();
        const issues: string[] = [];
        const labels = new Set<string>();

        for (const task of tasks) {
            if (!task.label || !task.command) {
                issues.push('Task is missing a label or command');
            }
            if (labels.has(task.label)) {
                issues.push(`Duplicate task label: ${task.label}`);
            }
            labels.add(task.label);
        }
        return { valid: issues.length === 0, issues };
    }

    async refreshTaskCache(): Promise<void> {
        this.categories.clear();
    }

    private normaliseCategory(category: string): string {
        if (category === 'javascript-react') {
            return 'react-development';
        }
        if (category === 'node-server') {
            return 'javascript-node';
        }
        return category;
    }

    private async loadCategory(categoryName: string): Promise<TaskCategory | null> {
        const category = this.normaliseCategory(categoryName);
        const cached = this.categories.get(category);
        if (cached) {
            return cached;
        }

        const relativePath = CATEGORY_PATHS[category];
        if (!relativePath) {
            return null;
        }

        const baseUrl = vscode.workspace
            .getConfiguration('smartTaskDetector')
            .get<string>(
                'taskRepositoryUrl',
                'https://raw.githubusercontent.com/DiogoRibeiro7/vscode-productivity-toolkit/main/tasks'
            )
            .replace(/\/$/, '');

        const loaded = await this.fetchJson<TaskCategory>(`${baseUrl}/${relativePath}`);
        loaded.category = this.normaliseCategory(loaded.category || category);
        this.categories.set(category, loaded);
        return loaded;
    }

    private fetchJson<T>(url: string): Promise<T> {
        return new Promise((resolve, reject) => {
            const request = https.get(url, { timeout: 10000 }, response => {
                const status = response.statusCode ?? 0;
                if (status < 200 || status >= 300) {
                    response.resume();
                    reject(new Error(`Task repository returned HTTP ${status}`));
                    return;
                }

                response.setEncoding('utf8');
                let body = '';
                response.on('data', chunk => {
                    body += chunk;
                });
                response.on('end', () => {
                    try {
                        resolve(JSON.parse(body) as T);
                    } catch (error) {
                        reject(new Error(`Invalid task repository response: ${String(error)}`));
                    }
                });
            });

            request.on('timeout', () => {
                request.destroy(new Error('Task repository request timed out'));
            });
            request.on('error', reject);
        });
    }

    private isTaskExport(value: unknown): value is { version: string; tasks: Task[] } {
        if (typeof value !== 'object' || value === null) {
            return false;
        }
        const candidate = value as { version?: unknown; tasks?: unknown };
        return typeof candidate.version === 'string' && Array.isArray(candidate.tasks);
    }
}
