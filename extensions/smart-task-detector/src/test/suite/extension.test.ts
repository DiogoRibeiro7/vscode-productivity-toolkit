import * as assert from 'assert';
import * as fs from 'fs-extra';
import * as path from 'path';
import * as vscode from 'vscode';

import { ProjectDetector } from '../../../services/ProjectDetector';

suite('Smart Task Detector', () => {
    let tempRoot: string;

    setup(async () => {
        tempRoot = path.join(__dirname, 'workspace-fixture');
        await fs.remove(tempRoot);
        await fs.ensureDir(tempRoot);
    });

    teardown(async () => {
        await fs.remove(tempRoot);
    });

    test('extension is discoverable and activates', async () => {
        const extension = vscode.extensions.getExtension('diogoribeiro7.smart-task-detector');
        assert.ok(extension, 'extension should be installed in the test host');

        await extension.activate();
        assert.strictEqual(extension.isActive, true);
    });

    test('commands are registered after activation', async () => {
        const extension = vscode.extensions.getExtension('diogoribeiro7.smart-task-detector');
        assert.ok(extension);
        await extension.activate();

        const commands = new Set(await vscode.commands.getCommands(true));
        for (const command of [
            'smartTaskDetector.detectAndInstall',
            'smartTaskDetector.openTaskManager',
            'smartTaskDetector.refreshTasks',
            'smartTaskDetector.installTask',
            'smartTaskDetector.removeTask',
            'smartTaskDetector.showWelcome'
        ]) {
            assert.ok(commands.has(command), `missing command: ${command}`);
        }
    });

    test('detects a Python workspace from files', async () => {
        await fs.writeFile(path.join(tempRoot, 'pyproject.toml'), '[project]\nname = "demo"\n');
        await fs.writeFile(path.join(tempRoot, 'main.py'), 'print("hello")\n');

        const detector = new ProjectDetector(tempRoot);
        const projects = await detector.detectProjectTypes();

        assert.ok(projects.some(project => project.type === 'python-general'));
    });

    test('handles an empty or missing workspace', async () => {
        const detector = new ProjectDetector(path.join(tempRoot, 'missing'));
        const projects = await detector.detectProjectTypes();

        assert.deepStrictEqual(projects, []);
    });
});
