import * as vscode from 'vscode';

export class WelcomeProvider {
    private context: vscode.ExtensionContext;
    private panel?: vscode.WebviewPanel;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
    }

    public show(): void {
        if (this.panel) {
            this.panel.reveal(vscode.ViewColumn.One);
            return;
        }

        this.panel = vscode.window.createWebviewPanel(
            'smartTaskDetectorWelcome',
            'Smart Task Detector - Welcome',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: []
            }
        );

        this.panel.webview.html = this.getWelcomeContent();

        this.panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.command) {
                    case 'detectAndInstall':
                        vscode.commands.executeCommand('smartTaskDetector.detectAndInstall');
                        break;
                    case 'openTaskManager':
                        vscode.commands.executeCommand('smartTaskDetector.openTaskManager');
                        break;
                    case 'openSettings':
                        vscode.commands.executeCommand('workbench.action.openSettings', 'smartTaskDetector');
                        break;
                    case 'dontShowAgain':
                        const config = vscode.workspace.getConfiguration('smartTaskDetector');
                        await config.update('showWelcomeOnFirstRun', false, vscode.ConfigurationTarget.Global);
                        vscode.window.showInformationMessage('Welcome screen disabled. You can re-enable it in settings.');
                        break;
                    case 'close':
                        this.panel?.dispose();
                        break;
                }
            },
            undefined,
            this.context.subscriptions
        );

        this.panel.onDidDispose(() => {
            this.panel = undefined;
        });
    }

    private getWelcomeContent(): string {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Task Detector - Welcome</title>
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
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .logo {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        h1 {
            color: var(--vscode-textLink-foreground);
            margin: 0 0 0.5rem 0;
            font-size: 2.5rem;
            font-weight: 300;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: var(--vscode-descriptionForeground);
            margin-bottom: 2rem;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .feature {
            background: var(--vscode-editor-inactiveSelectionBackground);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 8px;
            padding: 1.5rem;
        }
        
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
            display: block;
        }
        
        .feature h3 {
            margin: 0 0 1rem 0;
            color: var(--vscode-textLink-foreground);
        }
        
        .feature p {
            margin: 0;
            color: var(--vscode-descriptionForeground);
        }
        
        .actions {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin: 3rem 0;
        }
        
        .action-group {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }
        
        button {
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1rem;
            min-width: 200px;
            transition: background-color 0.2s;
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
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 2rem 0;
            padding: 1.5rem;
            background: var(--vscode-textBlockQuote-background);
            border-left: 4px solid var(--vscode-textLink-foreground);
            border-radius: 4px;
        }
        
        .stat {
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
        
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--vscode-panel-border);
            color: var(--vscode-descriptionForeground);
        }
        
        .dont-show {
            margin-top: 2rem;
            padding: 1rem;
            background: var(--vscode-editor-inactiveSelectionBackground);
            border-radius: 4px;
            text-align: center;
        }
        
        @media (max-width: 600px) {
            .container {
                padding: 1rem;
            }
            
            .action-group {
                flex-direction: column;
            }
            
            button {
                min-width: unset;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🚀</div>
            <h1>Smart Task Detector</h1>
            <p class="subtitle">
                Boost your productivity with intelligent task automation for VS Code
            </p>
        </div>

        <div class="stats">
            <div class="stat">
                <span class="stat-number">70+</span>
                <span class="stat-label">Ready-to-use Tasks</span>
            </div>
            <div class="stat">
                <span class="stat-number">9</span>
                <span class="stat-label">Technology Categories</span>
            </div>
            <div class="stat">
                <span class="stat-number">1-Click</span>
                <span class="stat-label">Installation</span>
            </div>
            <div class="stat">
                <span class="stat-number">Smart</span>
                <span class="stat-label">Auto-Detection</span>
            </div>
        </div>

        <div class="features">
            <div class="feature">
                <span class="feature-icon">🔍</span>
                <h3>Intelligent Detection</h3>
                <p>Automatically identifies your project type based on files, dependencies, and structure patterns.</p>
            </div>
            
            <div class="feature">
                <span class="feature-icon">⚡</span>
                <h3>One-Click Setup</h3>
                <p>Install all relevant productivity tasks for your tech stack with a single command.</p>
            </div>
            
            <div class="feature">
                <span class="feature-icon">🛡️</span>
                <h3>Safe & Secure</h3>
                <p>Automatic backup protection and security validation for all installed tasks.</p>
            </div>
            
            <div class="feature">
                <span class="feature-icon">🎯</span>
                <h3>Tech Stack Coverage</h3>
                <p>Python, JavaScript, React, Node.js, Docker, Git workflows, and system maintenance tasks.</p>
            </div>
        </div>

        <div class="actions">
            <h3>Get Started</h3>
            <div class="action-group">
                <button onclick="detectAndInstall()">
                    🔍 Detect & Install Tasks
                </button>
                <button onclick="openTaskManager()" class="secondary-button">
                    ⚙️ Open Task Manager
                </button>
            </div>
            
            <div class="action-group">
                <button onclick="openSettings()" class="secondary-button">
                    🛠️ Configure Settings
                </button>
                <button onclick="learnMore()" class="secondary-button">
                    📚 Learn More
                </button>
            </div>
        </div>

        <div class="dont-show">
            <p>Don't want to see this welcome screen again?</p>
            <button onclick="dontShowAgain()" class="secondary-button">
                Don't Show on Startup
            </button>
        </div>

        <div class="footer">
            <p>
                <strong>VS Code Productivity Toolkit</strong><br>
                Created by Diogo Ribeiro at ESMAD - Escola Superior de Média Arte e Design<br>
                Lead Data Scientist at Mysense.ai
            </p>
            <p style="margin-top: 1rem;">
                <a href="#" onclick="openExternal('https://github.com/DiogoRibeiro7/vscode-productivity-toolkit')" 
                   style="color: var(--vscode-textLink-foreground);">
                    GitHub Repository
                </a> • 
                <a href="#" onclick="openExternal('https://orcid.org/0009-0001-2022-7072')" 
                   style="color: var(--vscode-textLink-foreground);">
                    ORCID Profile
                </a>
            </p>
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();

        function detectAndInstall() {
            vscode.postMessage({ command: 'detectAndInstall' });
        }

        function openTaskManager() {
            vscode.postMessage({ command: 'openTaskManager' });
        }

        function openSettings() {
            vscode.postMessage({ command: 'openSettings' });
        }

        function dontShowAgain() {
            if (confirm('Are you sure you want to disable the welcome screen? You can re-enable it in the extension settings.')) {
                vscode.postMessage({ command: 'dontShowAgain' });
            }
        }

        function learnMore() {
            openExternal('https://github.com/DiogoRibeiro7/vscode-productivity-toolkit#readme');
        }

        function openExternal(url) {
            // In a real webview, you'd handle this differently
            // For now, we'll just show a message
            vscode.postMessage({ 
                command: 'showInformation', 
                text: 'Visit: ' + url 
            });
        }

        // Show a getting started tip
        setTimeout(() => {
            const tip = document.createElement('div');
            tip.style.cssText = \`
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: var(--vscode-notifications-background);
                border: 1px solid var(--vscode-notifications-border);
                padding: 1rem;
                border-radius: 4px;
                max-width: 300px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                z-index: 1000;
            \`;
            tip.innerHTML = \`
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="margin-right: 0.5rem;">💡</span>
                    <strong>Quick Tip</strong>
                </div>
                <p style="margin: 0; font-size: 0.9rem;">
                    Click "Detect & Install Tasks" to automatically set up productivity automation for your current project!
                </p>
                <button onclick="this.parentElement.remove()" 
                        style="margin-top: 0.5rem; font-size: 0.8rem; padding: 0.25rem 0.5rem;">
                    Got it
                </button>
            \`;
            document.body.appendChild(tip);
            
            // Auto-remove after 10 seconds
            setTimeout(() => {
                if (tip.parentElement) {
                    tip.remove();
                }
            }, 10000);
        }, 2000);
    </script>
</body>
</html>`;
    }
}
