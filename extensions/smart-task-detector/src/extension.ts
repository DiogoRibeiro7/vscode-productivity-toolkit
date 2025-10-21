/*
 * MIT License
 *
 * Copyright (c) 2025 Diogo Ribeiro
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

import * as vscode from 'vscode';
import * as path from 'path';
import { promises as fs } from 'fs';

interface ToolkitRecommendation {
  readonly id: string;
  readonly label: string;
  readonly description: string;
  readonly detail: string;
  readonly tasksFiles: string[];
  readonly extensionRecommendations: string[];
  detect(folder: vscode.WorkspaceFolder): Promise<boolean>;
}

interface DetectedRecommendation {
  readonly folder: vscode.WorkspaceFolder;
  readonly rule: ToolkitRecommendation;
}

type ToolkitTaskDefinition = Record<string, unknown>;
type ToolkitTaskInput = Record<string, unknown>;

interface ToolkitTaskFile {
  readonly version?: string;
  readonly tasks?: ToolkitTaskDefinition[];
  readonly inputs?: ToolkitTaskInput[];
  readonly _metadata?: Record<string, unknown>;
}

const outputChannel = vscode.window.createOutputChannel('Toolkit Smart Tasks');
let statusBarItem: vscode.StatusBarItem | undefined;
const detectionCache = new Map<string, DetectedRecommendation[]>();

function shouldLog(): boolean {
  const configuration = vscode.workspace.getConfiguration('vscodeProductivityToolkit');
  return configuration.get<boolean>('enableLogging', true);
}

function log(message: string): void {
  if (shouldLog()) {
    const timestamp = new Date().toISOString();
    outputChannel.appendLine(`[${timestamp}] ${message}`);
  }
}

const detectionRules: ToolkitRecommendation[] = [
  {
    id: 'python-data-science',
    label: 'Python Data Science',
    description: 'Notebook workflows, profiling, and Sphinx documentation.',
    detail: 'Detected notebooks, conda environments, or data-science packages.',
    tasksFiles: ['tasks/python/data-science.json'],
    extensionRecommendations: [
      'ms-python.python',
      'ms-toolsai.jupyter',
      'ms-python.vscode-pylance',
      'ms-toolsai.datawrangler'
    ],
    async detect(folder: vscode.WorkspaceFolder): Promise<boolean> {
      const notebooks = await vscode.workspace.findFiles(new vscode.RelativePattern(folder, '**/*.ipynb'), undefined, 5);
      if (notebooks.length > 0) {
        return true;
      }

      const environmentFiles = await vscode.workspace.findFiles(new vscode.RelativePattern(folder, '{environment.yml,environment.yaml,conda.yml}'), undefined, 1);
      if (environmentFiles.length > 0) {
        return true;
      }

      const requirementsPath = vscode.Uri.joinPath(folder.uri, 'requirements.txt');
      const hasDataPackages = await fileContainsAny(requirementsPath, ['pandas', 'numpy', 'scikit-learn', 'matplotlib']);
      return hasDataPackages;
    }
  },
  {
    id: 'python-general',
    label: 'Python General',
    description: 'Formatting, linting, testing, and packaging automation.',
    detail: 'Located pyproject.toml, setup.cfg, or Python modules.',
    tasksFiles: ['tasks/python/general.json'],
    extensionRecommendations: [
      'ms-python.python',
      'ms-python.vscode-pylance',
      'charliermarsh.ruff'
    ],
    async detect(folder: vscode.WorkspaceFolder): Promise<boolean> {
      const pyprojectFiles = await vscode.workspace.findFiles(new vscode.RelativePattern(folder, '{pyproject.toml,setup.cfg,setup.py}'), undefined, 1);
      if (pyprojectFiles.length > 0) {
        return true;
      }

      const pythonFiles = await vscode.workspace.findFiles(new vscode.RelativePattern(folder, '**/*.py'), undefined, 5);
      return pythonFiles.length > 0;
    }
  },
  {
    id: 'javascript-react',
    label: 'React + TypeScript',
    description: 'Storybook, Jest, bundle analysis, and Lighthouse audits.',
    detail: 'Found React dependencies or Vite/CRA scaffold.',
    tasksFiles: ['tasks/javascript/react.json'],
    extensionRecommendations: [
      'ms-vscode.vscode-typescript-next',
      'dbaeumer.vscode-eslint',
      'esbenp.prettier-vscode',
      'firsttris.vscode-jest-runner'
    ],
    async detect(folder: vscode.WorkspaceFolder): Promise<boolean> {
      const packageJson = await readPackageJson(folder);
      if (!packageJson) {
        return false;
      }

      const dependencies = {
        ...(packageJson.dependencies ?? {}),
        ...(packageJson.devDependencies ?? {})
      } as Record<string, string>;

      return Object.keys(dependencies).some((name) => ['react', 'next', 'vite'].includes(name));
    }
  },
  {
    id: 'javascript-node',
    label: 'Node Services',
    description: 'Express development, database migrations, and profiling.',
    detail: 'Detected Express/Fastify dependencies or server entry points.',
    tasksFiles: ['tasks/javascript/node.json'],
    extensionRecommendations: [
      'dbaeumer.vscode-eslint',
      'esbenp.prettier-vscode',
      'mongodb.mongodb-vscode',
      'ms-azuretools.vscode-docker'
    ],
    async detect(folder: vscode.WorkspaceFolder): Promise<boolean> {
      const packageJson = await readPackageJson(folder);
      if (!packageJson) {
        return false;
      }

      const dependencies = {
        ...(packageJson.dependencies ?? {}),
        ...(packageJson.devDependencies ?? {})
      } as Record<string, string>;

      if (Object.keys(dependencies).some((name) => ['express', 'fastify', 'hapi', 'koa'].includes(name))) {
        return true;
      }

      const apiFiles = await vscode.workspace.findFiles(new vscode.RelativePattern(folder, 'src/**/*.{ts,js}'), undefined, 5);
      return apiFiles.some((uri) => /server|api|app\.(ts|js)$/.test(uri.path));
    }
  }
];

async function readPackageJson(folder: vscode.WorkspaceFolder): Promise<Record<string, unknown> | undefined> {
  try {
    const packageUri = vscode.Uri.joinPath(folder.uri, 'package.json');
    const raw = await vscode.workspace.fs.readFile(packageUri);
    return JSON.parse(Buffer.from(raw).toString('utf8')) as Record<string, unknown>;
  } catch (error) {
    log(`No package.json detected for ${folder.name}: ${(error as Error).message}`);
    return undefined;
  }
}

async function fileContainsAny(uri: vscode.Uri, markers: string[]): Promise<boolean> {
  try {
    const raw = await vscode.workspace.fs.readFile(uri);
    const content = Buffer.from(raw).toString('utf8').toLowerCase();
    return markers.some((marker) => content.includes(marker.toLowerCase()));
  } catch (error) {
    log(`Unable to inspect ${uri.fsPath}: ${(error as Error).message}`);
    return false;
  }
}

async function ensureDirectory(directoryPath: string): Promise<void> {
  try {
    await fs.mkdir(directoryPath, { recursive: true });
  } catch (error) {
    log(`Failed to create directory ${directoryPath}: ${(error as Error).message}`);
    throw error;
  }
}

async function readTasksFile(uri: vscode.Uri): Promise<ToolkitTaskFile> {
  try {
    const raw = await vscode.workspace.fs.readFile(uri);
    const content = Buffer.from(raw).toString('utf8');
    return JSON.parse(content) as ToolkitTaskFile;
  } catch (error) {
    log(`Unable to parse tasks file ${uri.fsPath}: ${(error as Error).message}`);
    throw error;
  }
}

function mergeUnique<T extends Record<string, unknown>>(items: T[], key: keyof T): T[] {
  const seen = new Set<string>();
  const merged: T[] = [];
  for (const item of items) {
    const identifier = String(item[key] ?? JSON.stringify(item));
    if (!seen.has(identifier)) {
      seen.add(identifier);
      merged.push(item);
    }
  }
  return merged;
}

async function installRecommendations(recommendations: DetectedRecommendation[]): Promise<void> {
  if (recommendations.length === 0) {
    void vscode.window.showInformationMessage('No toolkit task recommendations are available to install.');
    return;
  }

  for (const { folder, rule } of recommendations) {
    try {
      log(`Installing ${rule.label} tasks for ${folder.name}`);
      await installTasksForFolder(folder, rule);
    } catch (error) {
      void vscode.window.showErrorMessage(`Toolkit installation failed for ${folder.name}: ${(error as Error).message}`);
      log(`Error installing tasks for ${folder.name}: ${(error as Error).stack ?? (error as Error).message}`);
    }
  }
}

async function installTasksForFolder(folder: vscode.WorkspaceFolder, rule: ToolkitRecommendation): Promise<void> {
  const workspaceRoot = folder.uri.fsPath;
  const vscodeDirectory = path.join(workspaceRoot, '.vscode');
  await ensureDirectory(vscodeDirectory);

  const tasksDestination = path.join(vscodeDirectory, 'tasks.json');
  const backupDestination = path.join(vscodeDirectory, `tasks.json.bak-${Date.now()}`);

  let existing: ToolkitTaskFile = { version: '2.0.0', tasks: [], inputs: [] };
  let shouldBackup = false;

  try {
    await fs.access(tasksDestination);
    shouldBackup = true;
    await fs.copyFile(tasksDestination, backupDestination);
    existing = await readTasksFile(vscode.Uri.file(tasksDestination));
  } catch (error) {
    log(`No existing tasks.json detected for ${folder.name}: ${(error as Error).message}`);
  }

  const aggregatedTasks: ToolkitTaskDefinition[] = Array.isArray(existing.tasks) ? [...existing.tasks] : [];
  const aggregatedInputs: ToolkitTaskInput[] = Array.isArray(existing.inputs) ? [...existing.inputs] : [];

  for (const relative of rule.tasksFiles) {
    const source = path.join(workspaceRoot, relative);
    try {
      const parsed = await readTasksFile(vscode.Uri.file(source));
      if (Array.isArray(parsed.tasks)) {
        aggregatedTasks.push(...parsed.tasks);
      }
      if (Array.isArray(parsed.inputs)) {
        aggregatedInputs.push(...parsed.inputs);
      }
    } catch (error) {
      log(`Unable to read ${relative}: ${(error as Error).message}`);
    }
  }

  const mergedTasks = mergeUnique(aggregatedTasks, 'label');
  const mergedInputs = mergeUnique(aggregatedInputs, 'id');

  const composed: ToolkitTaskFile = {
    _metadata: {
      license: 'MIT License - Copyright (c) 2025 Diogo Ribeiro',
      generatedBy: 'VS Code Productivity Toolkit Smart Task Detector',
      sourceRule: rule.id
    },
    version: existing.version ?? '2.0.0',
    tasks: mergedTasks,
    inputs: mergedInputs
  };

  await fs.writeFile(tasksDestination, `${JSON.stringify(composed, null, 2)}\n`, 'utf8');

  if (shouldBackup) {
    log(`Created backup at ${backupDestination}`);
  }

  await updateExtensionRecommendations(folder, rule.extensionRecommendations);
  void vscode.window.showInformationMessage(`Toolkit tasks installed for ${folder.name}: ${rule.label}`);
}

async function updateExtensionRecommendations(folder: vscode.WorkspaceFolder, recommendations: string[]): Promise<void> {
  if (recommendations.length === 0) {
    return;
  }

  const vscodeDirectory = path.join(folder.uri.fsPath, '.vscode');
  await ensureDirectory(vscodeDirectory);
  const recommendationsPath = path.join(vscodeDirectory, 'extensions.json');

  let existing: { recommendations?: string[]; _metadata?: Record<string, unknown> } = {};
  try {
    await fs.access(recommendationsPath);
    const raw = await fs.readFile(recommendationsPath, 'utf8');
    existing = JSON.parse(raw) as { recommendations?: string[]; _metadata?: Record<string, unknown> };
  } catch (error) {
    log(`Creating new extensions.json for ${folder.name}: ${(error as Error).message}`);
  }

  const mergedRecommendations = Array.from(new Set([...(existing.recommendations ?? []), ...recommendations]));
  const content = {
    _metadata: {
      license: 'MIT License - Copyright (c) 2025 Diogo Ribeiro',
      generatedBy: 'VS Code Productivity Toolkit Smart Task Detector'
    },
    recommendations: mergedRecommendations
  };

  await fs.writeFile(recommendationsPath, `${JSON.stringify(content, null, 2)}\n`, 'utf8');
}

async function detectAllRecommendations(): Promise<DetectedRecommendation[]> {
  const folders = vscode.workspace.workspaceFolders ?? [];
  const detections: DetectedRecommendation[] = [];

  for (const folder of folders) {
    for (const rule of detectionRules) {
      try {
        const isMatch = await rule.detect(folder);
        if (isMatch) {
          detections.push({ folder, rule });
        }
      } catch (error) {
        log(`Detection failed for ${rule.id} in ${folder.name}: ${(error as Error).message}`);
      }
    }
    detectionCache.set(folder.uri.toString(), detections.filter((item) => item.folder === folder));
  }

  return detections;
}

function updateStatusBar(detections: DetectedRecommendation[]): void {
  const configuration = vscode.workspace.getConfiguration('vscodeProductivityToolkit');
  if (!configuration.get<boolean>('statusBar', true)) {
    statusBarItem?.hide();
    return;
  }

  if (!statusBarItem) {
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBarItem.command = 'vscode-productivity-toolkit.showRecommendations';
  }

  if (detections.length === 0) {
    statusBarItem.text = '$(tools) Toolkit: No tasks suggested';
    statusBarItem.tooltip = 'Trigger detection to receive curated task recommendations.';
    statusBarItem.show();
    return;
  }

  const summary = detections.map((item) => item.rule.label).join(', ');
  statusBarItem.text = `$(tools) Toolkit: ${summary}`;
  statusBarItem.tooltip = 'Click to review and install recommended tasks.';
  statusBarItem.show();
}

async function handleDetectionLifecycle(): Promise<void> {
  const detections = await detectAllRecommendations();
  updateStatusBar(detections);

  if (detections.length === 0) {
    log('No recommendations discovered during detection run.');
    return;
  }

  const configuration = vscode.workspace.getConfiguration('vscodeProductivityToolkit');
  const autoInstall = configuration.get<boolean>('autoInstall', true);

  if (!autoInstall) {
    log('Auto-installation disabled by configuration.');
    return;
  }

  const installChoice = await vscode.window.showInformationMessage(
    `Toolkit detected ${detections.length} recommendation(s): ${detections.map((item) => item.rule.label).join(', ')}.`,
    'Install',
    'Not now'
  );

  if (installChoice === 'Install') {
    await installRecommendations(detections);
  }
}

async function promptForRecommendations(): Promise<void> {
  let detections = Array.from(detectionCache.values()).flat();
  if (detections.length === 0) {
    detections = await detectAllRecommendations();
  }

  if (detections.length === 0) {
    void vscode.window.showInformationMessage('No toolkit task recommendations are currently available.');
    return;
  }

  const quickPick = vscode.window.createQuickPick<vscode.QuickPickItem & { detection: DetectedRecommendation }>();
  quickPick.items = detections.map((detection) => ({
    label: detection.rule.label,
    description: detection.folder.name,
    detail: detection.rule.detail,
    picked: true,
    detection
  }));
  quickPick.canSelectMany = true;
  quickPick.title = 'Select toolkit task configurations to install';

  const selection = await new Promise<(vscode.QuickPickItem & { detection: DetectedRecommendation })[]>((resolve) => {
    quickPick.onDidAccept(() => {
      resolve(quickPick.selectedItems as (vscode.QuickPickItem & { detection: DetectedRecommendation })[]);
      quickPick.hide();
    });
    quickPick.onDidHide(() => {
      resolve([]);
    });
    quickPick.show();
  });

  if (selection.length === 0) {
    return;
  }

  await installRecommendations(selection.map((item) => item.detection));
}

export async function activate(context: vscode.ExtensionContext): Promise<void> {
  log('Activating VS Code Productivity Toolkit Smart Task Detector.');
  const detectCommand = vscode.commands.registerCommand('vscode-productivity-toolkit.detectTasks', handleDetectionLifecycle);
  const installCommand = vscode.commands.registerCommand('vscode-productivity-toolkit.installRecommendedTasks', async () => {
    const detections = Array.from(detectionCache.values()).flat();
    await installRecommendations(detections);
  });
  const showCommand = vscode.commands.registerCommand('vscode-productivity-toolkit.showRecommendations', promptForRecommendations);

  context.subscriptions.push(detectCommand, installCommand, showCommand, outputChannel);

  if (vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders.length > 0) {
    await handleDetectionLifecycle();
  } else {
    log('No workspace folders found during activation.');
  }
}

export function deactivate(): void {
  detectionCache.clear();
  statusBarItem?.dispose();
  outputChannel.dispose();
}
