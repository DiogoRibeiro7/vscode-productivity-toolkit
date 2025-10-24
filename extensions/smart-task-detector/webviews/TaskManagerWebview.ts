import * as vscode from 'vscode';
import { TaskManager, AvailableTask } from '../services/TaskManager';

export class TaskManagerWebview {
    private context: vscode.ExtensionContext;
    private taskManager: TaskManager;
    private panel?: vscode.WebviewPanel;

    constructor(context: vscode.ExtensionContext, taskManager: TaskManager) {
        this.context = context;
        this.taskManager = taskManager;
    }

    public show(): void {
        if (this.panel) {
            this.panel.reveal(vscode.ViewColumn.One);
            return;
        }

        this.panel = vscode.window.createWebviewPanel(
            'smartTaskDetectorManager',
            'Task Manager',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: []
            }
        );

        this.panel.webview.html = this.getWebviewContent();

        this.panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.command) {
                    case 'loadTasks':
                        await this.loadAndSendTasks();
                        break;
                    case 'installTask':
                        await this.installTask(message.task);
                        break;
                    case 'removeTask':
                        await this.removeTask(message.task);
                        break;
                    case 'installCategory':
                        await this.installCategory(message.category);
                        break;
                    case 'searchTasks':
                        await this.searchTasks(message.query);
                        break;
                    case 'exportTasks':
                        await this.exportTasks();
                        break;
                    case 'importTasks':
                        await this.importTasks();
                        break;
                    case 'validateTasks':
                        await this.validateTasks();
                        break;
                    case 'refreshTasks':
                        await this.refreshTasks();
                        break;
                }
            },
            undefined,
            this.context.subscriptions
        );

        this.panel.onDidDispose(() => {
            this.panel = undefined;
        });

        // Load initial data
        this.loadAndSendTasks();
    }

    private async loadAndSendTasks(): Promise<void> {
        try {
            const [allTasks, statistics, categories] = await Promise.all([
                this.taskManager.getAllAvailableTasks(),
                this.taskManager.getTaskStatistics(),
                this.taskManager.getTaskCategories()
            ]);

            this.panel?.webview.postMessage({
                command: 'tasksLoaded',
                data: {
                    tasks: allTasks,
                    statistics,
                    categories
                }
            });
        } catch (error) {
            console.error('Error loading tasks:', error);
            vscode.window.showErrorMessage('Failed to load tasks');
        }
    }

    private async installTask(task: AvailableTask): Promise<void> {
        try {
            await this.taskManager.taskInstaller.installTask(task);
            vscode.window.showInformationMessage(`Task "${task.label}" installed successfully!`);
            await this.loadAndSendTasks(); // Refresh
        } catch (error) {
            console.error('Error installing task:', error);
            vscode.window.showErrorMessage(`Failed to install task: ${error instanceof Error ? error.message : String(error)}`);
        }
    }

    private async removeTask(task: AvailableTask): Promise<void> {
        try {
            await this.taskManager.taskInstaller.removeTask(task);
            vscode.window.showInformationMessage(`Task "${task.label}" removed successfully!`);
            await this.loadAndSendTasks(); // Refresh
        } catch (error) {
            console.error('Error removing task:', error);
            vscode.window.showErrorMessage(`Failed to remove task: ${error instanceof Error ? error.message : String(error)}`);
        }
    }

    private async installCategory(categoryName: string): Promise<void> {
        try {
            await this.taskManager.installTasksByCategory(categoryName);
            vscode.window.showInformationMessage(`Category "${categoryName}" installed successfully!`);
            await this.loadAndSendTasks(); // Refresh
        } catch (error) {
            console.error('Error installing category:', error);
            vscode.window.showErrorMessage(`Failed to install category: ${error instanceof Error ? error.message : String(error)}`);
        }
    }

    private async searchTasks(query: string): Promise<void> {
        try {
            const searchResults = await this.taskManager.searchTasks(query);
            this.panel?.webview.postMessage({
                command: 'searchResults',
                data: {
                    query,
                    results: searchResults
                }
            });
        } catch (error) {
            console.error('Error searching tasks:', error);
            vscode.window.showErrorMessage('Failed to search tasks');
        }
    }

    private async exportTasks(): Promise<void> {
        try {
            const tasksJson = await this.taskManager.exportTasks();
            
            const saveUri = await vscode.window.showSaveDialog({
                defaultUri: vscode.Uri.file('vscode-tasks-export.json'),
                filters: {
                    'JSON Files': ['json'],
                    'All Files': ['*']
                }
            });

            if (saveUri) {
                await vscode.workspace.fs.writeFile(saveUri, Buffer.from(tasksJson, 'utf8'));
                vscode.window.showInformationMessage(`Tasks exported to ${saveUri.fsPath}`);
            }
        } catch (error) {
            console.error('Error exporting tasks:', error);
            vscode.window.showErrorMessage('Failed to export tasks');
        }
    }

    private async importTasks(): Promise<void> {
        try {
            const openUri = await vscode.window.showOpenDialog({
                canSelectFiles: true,
                canSelectFolders: false,
                canSelectMany: false,
                filters: {
                    'JSON Files': ['json'],
                    'All Files': ['*']
                }
            });

            if (openUri && openUri[0]) {
                const fileContent = await vscode.workspace.fs.readFile(openUri[0]);
                const tasksJson = Buffer.from(fileContent).toString('utf8');
                
                await this.taskManager.importTasks(tasksJson);
                vscode.window.showInformationMessage('Tasks imported successfully!');
                await this.loadAndSendTasks(); // Refresh
            }
        } catch (error) {
            console.error('Error importing tasks:', error);
            vscode.window.showErrorMessage(`Failed to import tasks: ${error instanceof Error ? error.message : String(error)}`);
        }
    }

    private async validateTasks(): Promise<void> {
        try {
            const validation = await this.taskManager.validateTaskIntegrity();
            
            this.panel?.webview.postMessage({
                command: 'validationResults',
                data: validation
            });

            if (validation.valid) {
                vscode.window.showInformationMessage('All tasks are valid!');
            } else {
                vscode.window.showWarningMessage(`Found ${validation.issues.length} task issues. Check the Task Manager for details.`);
            }
        } catch (error) {
            console.error('Error validating tasks:', error);
            vscode.window.showErrorMessage('Failed to validate tasks');
        }
    }

    private async refreshTasks(): Promise<void> {
        try {
            await this.taskManager.refreshTaskCache();
            await this.loadAndSendTasks();
            vscode.window.showInformationMessage('Tasks refreshed successfully!');
        } catch (error) {
            console.error('Error refreshing tasks:', error);
            vscode.window.showErrorMessage('Failed to refresh tasks');
        }
    }

    private getWebviewContent(): string {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
    <style>
        body {
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
            padding: 0;
            margin: 0;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--vscode-panel-border);
        }
        
        h1 {
            margin: 0;
            color: var(--vscode-textLink-foreground);
        }
        
        .controls {
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .search-box {
            padding: 0.5rem;
            border: 1px solid var(--vscode-input-border);
            background: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border-radius: 4px;
            min-width: 200px;
        }
        
        button {
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
        }
        
        button:hover {
            background: var(--vscode-button-hoverBackground);
        }
        
        .secondary-button {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
        }
        
        .secondary-button:hover {
            background: var(--vscode-button-secondaryHoverBackground);
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: var(--vscode-editor-inactiveSelectionBackground);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: var(--vscode-textLink-foreground);
            display: block;
        }
        
        .stat-label {
            color: var(--vscode-descriptionForeground);
            font-size: 0.9rem;
        }
        
        .tabs {
            display: flex;
            border-bottom: 1px solid var(--vscode-panel-border);
            margin-bottom: 1rem;
        }
        
        .tab {
            padding: 0.75rem 1.5rem;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            color: var(--vscode-descriptionForeground);
        }
        
        .tab.active {
            color: var(--vscode-textLink-foreground);
            border-bottom-color: var(--vscode-textLink-foreground);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .task-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1rem;
        }
        
        .task-card {
            background: var(--vscode-editor-inactiveSelectionBackground);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 8px;
            padding: 1rem;
            position: relative;
        }
        
        .task-card.installed {
            border-left: 4px solid var(--vscode-charts-green);
        }
        
        .task-card.available {
            border-left: 4px solid var(--vscode-charts-blue);
        }
        
        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.5rem;
        }
        
        .task-title {
            font-weight: bold;
            color: var(--vscode-textLink-foreground);
            margin: 0;
        }
        
        .task-status {
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .task-status.installed {
            background: var(--vscode-charts-green);
            color: white;
        }
        
        .task-status.available {
            background: var(--vscode-charts-blue);
            color: white;
        }
        
        .task-category {
            color: var(--vscode-descriptionForeground);
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        
        .task-command {
            font-family: var(--vscode-editor-font-family);
            background: var(--vscode-textCodeBlock-background);
            padding: 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            margin: 0.5rem 0;
            overflow-x: auto;
        }
        
        .task-actions {
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
        }
        
        .category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }
        
        .category-card {
            background: var(--vscode-editor-inactiveSelectionBackground);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 8px;
            padding: 1.5rem;
        }
        
        .category-title {
            font-weight: bold;
            color: var(--vscode-textLink-foreground);
            margin: 0 0 0.5rem 0;
        }
        
        .category-description {
            color: var(--vscode-descriptionForeground);
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }
        
        .category-stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
            color: var(--vscode-descriptionForeground);
        }
        
        .validation-results {
            margin-top: 1rem;
            padding: 1rem;
            border-radius: 4px;
        }
        
        .validation-results.valid {
            background: var(--vscode-inputValidation-infoBackground);
            border: 1px solid var(--vscode-inputValidation-infoBorder);
        }
        
        .validation-results.invalid {
            background: var(--vscode-inputValidation-warningBackground);
            border: 1px solid var(--vscode-inputValidation-warningBorder);
        }
        
        .issue-list {
            margin: 0.5rem 0;
            padding-left: 1rem;
        }
        
        @media (max-width: 768px) {
            .task-grid, .category-grid {
                grid-template-columns: 1fr;
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            .search-box {
                min-width: unset;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Task Manager</h1>
            <div class="controls">
                <input type="text" class="search-box" placeholder="Search tasks..." id="searchInput">
                <button onclick="refreshTasks()">🔄 Refresh</button>
                <button onclick="exportTasks()" class="secondary-button">📤 Export</button>
                <button onclick="importTasks()" class="secondary-button">📥 Import</button>
                <button onclick="validateTasks()" class="secondary-button">✅ Validate</button>
            </div>
        </div>

        <div class="stats" id="statsContainer">
            <div class="loading">Loading statistics...</div>
        </div>

        <div class="tabs">
            <div class="tab active" onclick="switchTab('tasks')">All Tasks</div>
            <div class="tab" onclick="switchTab('installed')">Installed</div>
            <div class="tab" onclick="switchTab('available')">Available</div>
            <div class="tab" onclick="switchTab('categories')">Categories</div>
        </div>

        <div class="tab-content active" id="tasks-content">
            <div class="task-grid" id="allTasksGrid">
                <div class="loading">Loading tasks...</div>
            </div>
        </div>

        <div class="tab-content" id="installed-content">
            <div class="task-grid" id="installedTasksGrid">
                <div class="loading">Loading installed tasks...</div>
            </div>
        </div>

        <div class="tab-content" id="available-content">
            <div class="task-grid" id="availableTasksGrid">
                <div class="loading">Loading available tasks...</div>
            </div>
        </div>

        <div class="tab-content" id="categories-content">
            <div class="category-grid" id="categoriesGrid">
                <div class="loading">Loading categories...</div>
            </div>
        </div>

        <div id="validationResults"></div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        let currentData = null;

        // Initialize
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.command) {
                case 'tasksLoaded':
                    currentData = message.data;
                    updateUI();
                    break;
                case 'searchResults':
                    displaySearchResults(message.data);
                    break;
                case 'validationResults':
                    displayValidationResults(message.data);
                    break;
            }
        });

        // Load initial data
        vscode.postMessage({ command: 'loadTasks' });

        // Tab switching
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabName + '-content').classList.add('active');
            
            if (currentData) {
                updateTabContent(tabName);
            }
        }

        // Search functionality
        document.getElementById('searchInput').addEventListener('input', (e) => {
            const query = e.target.value.trim();
            if (query.length > 2) {
                vscode.postMessage({ command: 'searchTasks', query });
            } else if (query.length === 0 && currentData) {
                updateUI();
            }
        });

        function updateUI() {
            if (!currentData) return;

            updateStats();
            updateTabContent('tasks');
            updateTabContent('installed');
            updateTabContent('available');
            updateTabContent('categories');
        }

        function updateStats() {
            const stats = currentData.statistics;
            const statsContainer = document.getElementById('statsContainer');
            
            statsContainer.innerHTML = \`
                <div class="stat-card">
                    <span class="stat-number">\${stats.totalAvailable}</span>
                    <span class="stat-label">Total Available</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">\${stats.totalInstalled}</span>
                    <span class="stat-label">Installed</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">\${stats.categoriesAvailable}</span>
                    <span class="stat-label">Categories</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">\${Math.round((stats.totalInstalled / stats.totalAvailable) * 100)}%</span>
                    <span class="stat-label">Coverage</span>
                </div>
            \`;
        }

        function updateTabContent(tabName) {
            switch (tabName) {
                case 'tasks':
                    displayTasks('allTasksGrid', currentData.tasks);
                    break;
                case 'installed':
                    displayTasks('installedTasksGrid', currentData.tasks.filter(t => t.isInstalled));
                    break;
                case 'available':
                    displayTasks('availableTasksGrid', currentData.tasks.filter(t => !t.isInstalled));
                    break;
                case 'categories':
                    displayCategories('categoriesGrid', currentData.categories);
                    break;
            }
        }

        function displayTasks(containerId, tasks) {
            const container = document.getElementById(containerId);
            
            if (tasks.length === 0) {
                container.innerHTML = '<div class="loading">No tasks found</div>';
                return;
            }

            container.innerHTML = tasks.map(task => \`
                <div class="task-card \${task.isInstalled ? 'installed' : 'available'}">
                    <div class="task-header">
                        <h3 class="task-title">\${task.label}</h3>
                        <span class="task-status \${task.isInstalled ? 'installed' : 'available'}">
                            \${task.isInstalled ? 'Installed' : 'Available'}
                        </span>
                    </div>
                    <div class="task-category">Category: \${task.category}</div>
                    <div class="task-command">\${task.command} \${task.args ? task.args.join(' ') : ''}</div>
                    <div class="task-actions">
                        \${task.isInstalled 
                            ? \`<button onclick="removeTask('\${task.label}')" class="secondary-button">Remove</button>
                               <button onclick="runTask('\${task.label}')">Run Task</button>\`
                            : \`<button onclick="installTask('\${task.label}')">Install</button>\`
                        }
                    </div>
                </div>
            \`).join('');
        }

        function displayCategories(containerId, categories) {
            const container = document.getElementById(containerId);
            
            container.innerHTML = categories.map(category => {
                const installedCount = currentData.tasks.filter(t => 
                    t.category === category.category && t.isInstalled
                ).length;
                
                return \`
                    <div class="category-card">
                        <h3 class="category-title">\${category.displayName}</h3>
                        <div class="category-description">\${category.description}</div>
                        <div class="category-stats">
                            <span>Tasks: \${category.tasks.length}</span>
                            <span>Installed: \${installedCount}</span>
                        </div>
                        <button onclick="installCategory('\${category.category}')">
                            Install All (\${category.tasks.length - installedCount} remaining)
                        </button>
                    </div>
                \`;
            }).join('');
        }

        function displaySearchResults(data) {
            // Update the current active tab with search results
            const activeTab = document.querySelector('.tab.active').textContent.toLowerCase();
            if (activeTab.includes('task')) {
                displayTasks('allTasksGrid', data.results);
            }
        }

        function displayValidationResults(validation) {
            const container = document.getElementById('validationResults');
            
            container.innerHTML = \`
                <div class="validation-results \${validation.valid ? 'valid' : 'invalid'}">
                    <h3>\${validation.valid ? '✅ All tasks are valid!' : '⚠️ Task validation issues found'}</h3>
                    \${validation.issues.length > 0 ? \`
                        <ul class="issue-list">
                            \${validation.issues.map(issue => \`<li>\${issue}</li>\`).join('')}
                        </ul>
                    \` : ''}
                </div>
            \`;
        }

        // Task actions
        function installTask(label) {
            const task = currentData.tasks.find(t => t.label === label);
            if (task) {
                vscode.postMessage({ command: 'installTask', task });
            }
        }

        function removeTask(label) {
            const task = currentData.tasks.find(t => t.label === label);
            if (task && confirm(\`Are you sure you want to remove "\${label}"?\`)) {
                vscode.postMessage({ command: 'removeTask', task });
            }
        }

        function runTask(label) {
            // This would run the task in VS Code
            vscode.postMessage({ command: 'runTask', label });
        }

        function installCategory(category) {
            vscode.postMessage({ command: 'installCategory', category });
        }

        // Menu actions
        function refreshTasks() {
            vscode.postMessage({ command: 'refreshTasks' });
        }

        function exportTasks() {
            vscode.postMessage({ command: 'exportTasks' });
        }

        function importTasks() {
            vscode.postMessage({ command: 'importTasks' });
        }

        function validateTasks() {
            vscode.postMessage({ command: 'validateTasks' });
        }
    </script>
</body>
</html>`;
    }
}
