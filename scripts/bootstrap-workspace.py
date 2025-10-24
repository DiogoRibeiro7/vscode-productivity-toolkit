#!/usr/bin/env python3
"""
VS Code Productivity Toolkit - Workspace Bootstrap Script

This script automatically detects your project type and installs relevant productivity tasks
for VS Code, enhancing your development workflow with one-click automation.

Author: Diogo Ribeiro (dfr@esmad.ipp.pt)
License: MIT
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import argparse
import urllib.request
import urllib.error

class ProjectDetector:
    """Detects project types based on file patterns and dependencies."""
    
    DETECTION_RULES = {
        'python-general': {
            'files': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
            'extensions': ['.py'],
            'confidence_threshold': 0.3
        },
        'python-data-science': {
            'files': ['environment.yml', 'conda.yml'],
            'extensions': ['.ipynb'],
            'dependencies': ['pandas', 'numpy', 'matplotlib', 'jupyter']
        },
        'javascript-general': {
            'files': ['package.json', 'tsconfig.json'],
            'extensions': ['.js', '.ts']
        },
        'react-development': {
            'files': ['package.json'],
            'directories': ['src'],
            'react_indicators': ['src/App.jsx', 'src/App.tsx', 'public/index.html']
        },
        'node-server': {
            'files': ['package.json'],
            'server_files': ['server.js', 'app.js', 'index.js']
        },
        'docker-general': {
            'files': ['Dockerfile', '.dockerignore']
        },
        'docker-compose': {
            'files': ['docker-compose.yml', 'docker-compose.yaml']
        },
        'git-workflows': {
            'directories': ['.git'],
            'files': ['.gitignore', '.github']
        }
    }

    def __init__(self, project_path: str = '.'):
        self.project_path = Path(project_path).resolve()

    def detect_project_types(self) -> List[str]:
        """Detect all applicable project types for the current directory."""
        detected_types = []
        
        for project_type, rules in self.DETECTION_RULES.items():
            if self._matches_rules(rules):
                detected_types.append(project_type)
                print(f"✓ Detected: {project_type}")
        
        return detected_types

    def _matches_rules(self, rules: Dict[str, Any]) -> bool:
        """Check if current project matches the given rules."""
        score = 0
        max_score = 0
        
        # Check for required files
        if 'files' in rules:
            for file_name in rules['files']:
                max_score += 1
                if (self.project_path / file_name).exists():
                    score += 1
        
        # Check for file extensions
        if 'extensions' in rules:
            max_score += 1
            if self._has_files_with_extensions(rules['extensions']):
                score += 1
        
        # Check for directories
        if 'directories' in rules:
            for dir_name in rules['directories']:
                max_score += 1
                if (self.project_path / dir_name).exists():
                    score += 1
        
        # Special checks for React
        if 'react_indicators' in rules:
            max_score += 1
            if any((self.project_path / indicator).exists() for indicator in rules['react_indicators']):
                score += 1
        
        # Special checks for Node server
        if 'server_files' in rules:
            max_score += 1
            if any((self.project_path / server_file).exists() for server_file in rules['server_files']):
                score += 1
        
        # Check dependencies for Python projects
        if 'dependencies' in rules:
            max_score += 1
            if self._check_python_dependencies(rules['dependencies']):
                score += 1
        
        confidence = score / max_score if max_score > 0 else 0
        threshold = rules.get('confidence_threshold', 0.5)
        
        return confidence >= threshold

    def _has_files_with_extensions(self, extensions: List[str]) -> bool:
        """Check if project has files with specified extensions."""
        for ext in extensions:
            if list(self.project_path.rglob(f'*{ext}')):
                return True
        return False

    def _check_python_dependencies(self, dependencies: List[str]) -> bool:
        """Check if Python project has specified dependencies."""
        # Check requirements.txt
        req_file = self.project_path / 'requirements.txt'
        if req_file.exists():
            content = req_file.read_text().lower()
            found = sum(1 for dep in dependencies if dep.lower() in content)
            return found >= len(dependencies) * 0.5
        
        # Check setup.py
        setup_file = self.project_path / 'setup.py'
        if setup_file.exists():
            content = setup_file.read_text().lower()
            found = sum(1 for dep in dependencies if dep.lower() in content)
            return found >= len(dependencies) * 0.5
        
        return False

class TaskInstaller:
    """Installs VS Code tasks based on detected project types."""
    
    def __init__(self, project_path: str = '.'):
        self.project_path = Path(project_path).resolve()
        self.vscode_path = self.project_path / '.vscode'
        self.tasks_file = self.vscode_path / 'tasks.json'

    def install_tasks_for_types(self, project_types: List[str], task_source: str = 'local') -> None:
        """Install tasks for the detected project types."""
        print(f"\n📦 Installing tasks for: {', '.join(project_types)}")
        
        all_tasks = []
        
        for project_type in project_types:
            try:
                tasks = self._load_tasks_for_type(project_type, task_source)
                if tasks:
                    all_tasks.extend(tasks)
                    print(f"✓ Loaded {len(tasks)} tasks for {project_type}")
                else:
                    print(f"⚠ No tasks found for {project_type}")
            except Exception as e:
                print(f"❌ Error loading tasks for {project_type}: {e}")
        
        if all_tasks:
            self._write_tasks_file(all_tasks)
            print(f"\n🎉 Successfully installed {len(all_tasks)} tasks!")
        else:
            print("\n⚠ No tasks were installed.")

    def _load_tasks_for_type(self, project_type: str, source: str) -> List[Dict[str, Any]]:
        """Load tasks for a specific project type."""
        if source == 'local':
            return self._load_local_tasks(project_type)
        else:
            return self._load_remote_tasks(project_type, source)

    def _load_local_tasks(self, project_type: str) -> List[Dict[str, Any]]:
        """Load tasks from local files."""
        # Map project types to file paths
        type_to_file = {
            'python-general': 'tasks/python/general.json',
            'python-data-science': 'tasks/python/data-science.json',
            'javascript-general': 'tasks/javascript/general.json',
            'react-development': 'tasks/javascript/react.json',
            'node-server': 'tasks/javascript/node.json',
            'docker-general': 'tasks/docker/general.json',
            'docker-compose': 'tasks/docker/compose.json',
            'git-workflows': 'tasks/git/workflows.json'
        }
        
        task_file = type_to_file.get(project_type)
        if not task_file:
            return []
        
        # Try to find the task file in various locations
        possible_paths = [
            Path(__file__).parent.parent / task_file,  # Relative to script
            Path.cwd() / task_file,  # Current directory
            Path.home() / '.vscode-productivity-toolkit' / task_file  # Home directory
        ]
        
        for path in possible_paths:
            if path.exists():
                try:
                    with open(path, 'r') as f:
                        task_data = json.load(f)
                        return task_data.get('tasks', [])
                except Exception as e:
                    print(f"Error reading {path}: {e}")
        
        return []

    def _load_remote_tasks(self, project_type: str, base_url: str) -> List[Dict[str, Any]]:
        """Load tasks from remote repository."""
        type_to_file = {
            'python-general': 'python/general.json',
            'python-data-science': 'python/data-science.json',
            'javascript-general': 'javascript/general.json',
            'react-development': 'javascript/react.json',
            'node-server': 'javascript/node.json',
            'docker-general': 'docker/general.json',
            'docker-compose': 'docker/compose.json',
            'git-workflows': 'git/workflows.json'
        }
        
        task_file = type_to_file.get(project_type)
        if not task_file:
            return []
        
        url = f"{base_url.rstrip('/')}/{task_file}"
        
        try:
            with urllib.request.urlopen(url) as response:
                task_data = json.loads(response.read().decode())
                return task_data.get('tasks', [])
        except urllib.error.URLError as e:
            print(f"Failed to download tasks from {url}: {e}")
            return []

    def _write_tasks_file(self, tasks: List[Dict[str, Any]]) -> None:
        """Write tasks to VS Code tasks.json file."""
        # Ensure .vscode directory exists
        self.vscode_path.mkdir(exist_ok=True)
        
        # Read existing tasks if file exists
        existing_tasks = []
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    existing_data = json.load(f)
                    existing_tasks = existing_data.get('tasks', [])
            except Exception as e:
                print(f"Warning: Could not read existing tasks.json: {e}")
        
        # Merge tasks (avoid duplicates by label)
        existing_labels = {task.get('label') for task in existing_tasks}
        new_tasks = [task for task in tasks if task.get('label') not in existing_labels]
        
        all_tasks = existing_tasks + new_tasks
        
        # Create tasks.json structure
        tasks_config = {
            "version": "2.0.0",
            "tasks": all_tasks
        }
        
        # Write to file
        with open(self.tasks_file, 'w') as f:
            json.dump(tasks_config, f, indent=4)

def main():
    """Main entry point for the bootstrap script."""
    parser = argparse.ArgumentParser(
        description='Bootstrap VS Code workspace with productivity tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bootstrap-workspace.py                    # Auto-detect and install
  python bootstrap-workspace.py --types python    # Install only Python tasks
  python bootstrap-workspace.py --list            # List detected project types
  python bootstrap-workspace.py --remote          # Use remote task repository
        """
    )
    
    parser.add_argument('--types', nargs='+', help='Specific project types to install tasks for')
    parser.add_argument('--list', action='store_true', help='List detected project types and exit')
    parser.add_argument('--remote', action='store_true', help='Download tasks from remote repository')
    parser.add_argument('--path', default='.', help='Project path (default: current directory)')
    parser.add_argument('--task-repo', default='https://raw.githubusercontent.com/DiogoRibeiro7/vscode-productivity-toolkit/main/tasks',
                       help='Remote task repository URL')
    
    args = parser.parse_args()
    
    print("🚀 VS Code Productivity Toolkit - Workspace Bootstrap")
    print("=" * 55)
    
    # Initialize detector
    detector = ProjectDetector(args.path)
    
    # Detect project types
    print(f"🔍 Analyzing project at: {detector.project_path}")
    detected_types = detector.detect_project_types()
    
    if not detected_types:
        print("\n❌ No recognized project types found.")
        print("Supported types: python, javascript, react, node, docker, git")
        return 1
    
    if args.list:
        print(f"\n📋 Detected project types: {', '.join(detected_types)}")
        return 0
    
    # Determine which types to install
    types_to_install = args.types if args.types else detected_types
    
    # Validate types
    valid_types = set(detector.DETECTION_RULES.keys())
    invalid_types = [t for t in types_to_install if t not in valid_types]
    if invalid_types:
        print(f"❌ Invalid project types: {', '.join(invalid_types)}")
        print(f"Valid types: {', '.join(sorted(valid_types))}")
        return 1
    
    # Install tasks
    installer = TaskInstaller(args.path)
    task_source = args.task_repo if args.remote else 'local'
    
    try:
        installer.install_tasks_for_types(types_to_install, task_source)
        print(f"\n✨ Bootstrap complete! Open VS Code and check the Tasks menu.")
        return 0
    except Exception as e:
        print(f"\n❌ Bootstrap failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
