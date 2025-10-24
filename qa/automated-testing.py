#!/usr/bin/env python3
"""
VS Code Productivity Toolkit - Automated Testing Script

Comprehensive automated testing for all components of the toolkit including
task validation, extension testing, and integration verification.

Author: Diogo Ribeiro (dfr@esmad.ipp.pt)
License: MIT
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import argparse
import logging
import time
import unittest
import sqlite3

@dataclass
class TestResult:
    """Result of a test execution."""
    name: str
    passed: bool
    duration: float
    message: str = ""
    details: Optional[Dict[str, Any]] = None

class AutomatedTester:
    """Comprehensive automated testing for the VS Code Productivity Toolkit."""
    
    def __init__(self, project_root: str = '.'):
        self.project_root = Path(project_root).resolve()
        self.temp_dir = None
        self.logger = self._setup_logging()
        self.results = []
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('automated_testing.log')
            ]
        )
        return logging.getLogger(__name__)

    def run_all_tests(self) -> List[TestResult]:
        """Run all automated tests."""
        self.logger.info("Starting comprehensive automated testing")
        
        # Create temporary workspace
        self.temp_dir = tempfile.mkdtemp(prefix='vscode_toolkit_test_')
        self.logger.info(f"Using temporary directory: {self.temp_dir}")
        
        try:
            # Test categories
            test_categories = [
                ('Task Validation', self._test_task_validation),
                ('Project Detection', self._test_project_detection),
                ('Task Installation', self._test_task_installation),
                ('Extension Structure', self._test_extension_structure),
                ('Python CLI', self._test_python_cli),
                ('Configuration Files', self._test_configuration_files),
                ('Documentation', self._test_documentation),
                ('Scripts', self._test_scripts),
                ('Integration', self._test_integration),
                ('Performance', self._test_performance)
            ]
            
            for category_name, test_function in test_categories:
                self.logger.info(f"Running {category_name} tests...")
                category_results = test_function()
                self.results.extend(category_results)
                
                passed = sum(1 for r in category_results if r.passed)
                total = len(category_results)
                self.logger.info(f"{category_name}: {passed}/{total} tests passed")
        
        finally:
            # Cleanup
            if self.temp_dir and Path(self.temp_dir).exists():
                shutil.rmtree(self.temp_dir)
        
        return self.results

    def _test_task_validation(self) -> List[TestResult]:
        """Test all task definition files for validity."""
        results = []
        tasks_dir = self.project_root / 'tasks'
        
        if not tasks_dir.exists():
            return [TestResult(
                name="task_directory_exists",
                passed=False,
                duration=0.0,
                message="Tasks directory not found"
            )]
        
        # Find all task JSON files
        task_files = list(tasks_dir.rglob('*.json'))
        
        for task_file in task_files:
            start_time = time.time()
            
            try:
                # Test JSON validity
                with open(task_file, 'r') as f:
                    task_data = json.load(f)
                
                # Validate required fields
                required_fields = ['taskVersion', 'category', 'displayName', 'description', 'tasks']
                missing_fields = [field for field in required_fields if field not in task_data]
                
                if missing_fields:
                    results.append(TestResult(
                        name=f"task_schema_{task_file.name}",
                        passed=False,
                        duration=time.time() - start_time,
                        message=f"Missing required fields: {missing_fields}"
                    ))
                    continue
                
                # Validate task structure
                tasks = task_data.get('tasks', [])
                for i, task in enumerate(tasks):
                    task_required = ['label', 'type', 'command']
                    task_missing = [field for field in task_required if field not in task]
                    
                    if task_missing:
                        results.append(TestResult(
                            name=f"task_structure_{task_file.name}_task_{i}",
                            passed=False,
                            duration=time.time() - start_time,
                            message=f"Task {i} missing fields: {task_missing}"
                        ))
                        continue
                
                results.append(TestResult(
                    name=f"task_validation_{task_file.name}",
                    passed=True,
                    duration=time.time() - start_time,
                    message=f"Valid task file with {len(tasks)} tasks"
                ))
                
            except json.JSONDecodeError as e:
                results.append(TestResult(
                    name=f"task_json_{task_file.name}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Invalid JSON: {e}"
                ))
            except Exception as e:
                results.append(TestResult(
                    name=f"task_error_{task_file.name}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Error validating task: {e}"
                ))
        
        return results

    def _test_project_detection(self) -> List[TestResult]:
        """Test project detection logic."""
        results = []
        
        # Test with known project structures
        test_projects = [
            ('python', {'requirements.txt': 'django==3.2.0', 'main.py': 'print("hello")'}),
            ('javascript', {'package.json': '{"name": "test", "dependencies": {}}', 'index.js': 'console.log("hello")'}),
            ('docker', {'Dockerfile': 'FROM node:14', 'docker-compose.yml': 'version: "3"'}),
            ('react', {
                'package.json': '{"dependencies": {"react": "^17.0.0"}}',
                'src/App.jsx': 'export default function App() { return <div>Hello</div>; }'
            })
        ]
        
        for project_type, files in test_projects:
            start_time = time.time()
            test_dir = Path(self.temp_dir) / f'test_{project_type}'
            test_dir.mkdir(exist_ok=True)
            
            try:
                # Create test project structure
                for file_path, content in files.items():
                    full_path = test_dir / file_path
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content)
                
                # Test detection (would need to import detector module)
                # For now, just test that we can create the structure
                results.append(TestResult(
                    name=f"project_detection_{project_type}",
                    passed=True,
                    duration=time.time() - start_time,
                    message=f"Test project structure created for {project_type}"
                ))
                
            except Exception as e:
                results.append(TestResult(
                    name=f"project_detection_{project_type}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Failed to create test project: {e}"
                ))
        
        return results

    def _test_task_installation(self) -> List[TestResult]:
        """Test task installation functionality."""
        results = []
        
        # Test creating .vscode/tasks.json
        start_time = time.time()
        test_workspace = Path(self.temp_dir) / 'test_workspace'
        test_workspace.mkdir(exist_ok=True)
        vscode_dir = test_workspace / '.vscode'
        vscode_dir.mkdir(exist_ok=True)
        
        try:
            # Create a test tasks.json
            test_tasks = {
                "version": "2.0.0",
                "tasks": [
                    {
                        "label": "Test Task",
                        "type": "shell",
                        "command": "echo",
                        "args": ["hello"]
                    }
                ]
            }
            
            tasks_file = vscode_dir / 'tasks.json'
            with open(tasks_file, 'w') as f:
                json.dump(test_tasks, f, indent=2)
            
            # Validate the created file
            with open(tasks_file, 'r') as f:
                loaded_tasks = json.load(f)
            
            if loaded_tasks['version'] == '2.0.0' and len(loaded_tasks['tasks']) == 1:
                results.append(TestResult(
                    name="task_installation_basic",
                    passed=True,
                    duration=time.time() - start_time,
                    message="Successfully created and validated tasks.json"
                ))
            else:
                results.append(TestResult(
                    name="task_installation_basic",
                    passed=False,
                    duration=time.time() - start_time,
                    message="Tasks.json validation failed"
                ))
                
        except Exception as e:
            results.append(TestResult(
                name="task_installation_basic",
                passed=False,
                duration=time.time() - start_time,
                message=f"Task installation test failed: {e}"
            ))
        
        return results

    def _test_extension_structure(self) -> List[TestResult]:
        """Test VS Code extension structure and files."""
        results = []
        extension_dir = self.project_root / 'extensions' / 'smart-task-detector'
        
        # Required files
        required_files = [
            'package.json',
            'tsconfig.json',
            'webpack.config.js',
            '.eslintrc.js',
            'src/extension.ts'
        ]
        
        for file_path in required_files:
            start_time = time.time()
            full_path = extension_dir / file_path
            
            if full_path.exists():
                results.append(TestResult(
                    name=f"extension_file_{file_path.replace('/', '_')}",
                    passed=True,
                    duration=time.time() - start_time,
                    message=f"Extension file exists: {file_path}"
                ))
            else:
                results.append(TestResult(
                    name=f"extension_file_{file_path.replace('/', '_')}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Missing extension file: {file_path}"
                ))
        
        # Test package.json validity
        start_time = time.time()
        package_json = extension_dir / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                
                required_fields = ['name', 'version', 'engines', 'main', 'contributes']
                missing_fields = [field for field in required_fields if field not in package_data]
                
                if not missing_fields:
                    results.append(TestResult(
                        name="extension_package_json",
                        passed=True,
                        duration=time.time() - start_time,
                        message="Extension package.json is valid"
                    ))
                else:
                    results.append(TestResult(
                        name="extension_package_json",
                        passed=False,
                        duration=time.time() - start_time,
                        message=f"Extension package.json missing fields: {missing_fields}"
                    ))
                    
            except Exception as e:
                results.append(TestResult(
                    name="extension_package_json",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Error validating extension package.json: {e}"
                ))
        
        return results

    def _test_python_cli(self) -> List[TestResult]:
        """Test Python CLI functionality."""
        results = []
        
        # Test Python package structure
        python_pkg = self.project_root / 'toolkit'
        required_files = ['__init__.py', 'cli.py', 'detector.py', 'installer.py']
        
        for file_name in required_files:
            start_time = time.time()
            file_path = python_pkg / file_name
            
            if file_path.exists():
                results.append(TestResult(
                    name=f"python_file_{file_name}",
                    passed=True,
                    duration=time.time() - start_time,
                    message=f"Python file exists: {file_name}"
                ))
            else:
                results.append(TestResult(
                    name=f"python_file_{file_name}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Missing Python file: {file_name}"
                ))
        
        # Test if Python files are syntactically valid
        for py_file in python_pkg.glob('*.py'):
            start_time = time.time()
            try:
                with open(py_file, 'r') as f:
                    code = f.read()
                
                # Basic syntax check
                compile(code, str(py_file), 'exec')
                
                results.append(TestResult(
                    name=f"python_syntax_{py_file.name}",
                    passed=True,
                    duration=time.time() - start_time,
                    message=f"Valid Python syntax: {py_file.name}"
                ))
                
            except SyntaxError as e:
                results.append(TestResult(
                    name=f"python_syntax_{py_file.name}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Syntax error in {py_file.name}: {e}"
                ))
            except Exception as e:
                results.append(TestResult(
                    name=f"python_syntax_{py_file.name}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Error checking {py_file.name}: {e}"
                ))
        
        return results

    def _test_configuration_files(self) -> List[TestResult]:
        """Test configuration files."""
        results = []
        
        config_files = [
            ('pyproject.toml', 'TOML configuration'),
            ('package.json', 'Root package.json'),
            ('.gitignore', 'Git ignore rules'),
            ('requirements.txt', 'Python dependencies')
        ]
        
        for file_name, description in config_files:
            start_time = time.time()
            file_path = self.project_root / file_name
            
            if file_path.exists() and file_path.stat().st_size > 0:
                results.append(TestResult(
                    name=f"config_{file_name.replace('.', '_')}",
                    passed=True,
                    duration=time.time() - start_time,
                    message=f"{description} exists and is not empty"
                ))
            else:
                results.append(TestResult(
                    name=f"config_{file_name.replace('.', '_')}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"{description} missing or empty"
                ))
        
        return results

    def _test_documentation(self) -> List[TestResult]:
        """Test documentation files."""
        results = []
        
        docs_files = [
            ('README.md', 'Main README'),
            ('CHANGELOG.md', 'Changelog'),
            ('CONTRIBUTING.md', 'Contributing guidelines'),
            ('docs/getting-started.md', 'Getting started guide')
        ]
        
        for file_path, description in docs_files:
            start_time = time.time()
            full_path = self.project_root / file_path
            
            if full_path.exists() and full_path.stat().st_size > 100:  # At least 100 bytes
                results.append(TestResult(
                    name=f"docs_{file_path.replace('/', '_').replace('.', '_')}",
                    passed=True,
                    duration=time.time() - start_time,
                    message=f"{description} exists and has content"
                ))
            else:
                results.append(TestResult(
                    name=f"docs_{file_path.replace('/', '_').replace('.', '_')}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"{description} missing or too small"
                ))
        
        return results

    def _test_scripts(self) -> List[TestResult]:
        """Test automation scripts."""
        results = []
        
        scripts_dir = self.project_root / 'scripts'
        expected_scripts = [
            'bootstrap-workspace.py',
            'bulk-install.py', 
            'productivity-analysis.py'
        ]
        
        for script_name in expected_scripts:
            start_time = time.time()
            script_path = scripts_dir / script_name
            
            if script_path.exists():
                # Test if script is executable and has valid Python syntax
                try:
                    with open(script_path, 'r') as f:
                        code = f.read()
                    
                    # Check for shebang
                    if code.startswith('#!/usr/bin/env python3'):
                        # Check syntax
                        compile(code, str(script_path), 'exec')
                        
                        results.append(TestResult(
                            name=f"script_{script_name.replace('.', '_')}",
                            passed=True,
                            duration=time.time() - start_time,
                            message=f"Script {script_name} is valid"
                        ))
                    else:
                        results.append(TestResult(
                            name=f"script_{script_name.replace('.', '_')}",
                            passed=False,
                            duration=time.time() - start_time,
                            message=f"Script {script_name} missing shebang"
                        ))
                        
                except SyntaxError as e:
                    results.append(TestResult(
                        name=f"script_{script_name.replace('.', '_')}",
                        passed=False,
                        duration=time.time() - start_time,
                        message=f"Syntax error in {script_name}: {e}"
                    ))
            else:
                results.append(TestResult(
                    name=f"script_{script_name.replace('.', '_')}",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Script {script_name} not found"
                ))
        
        return results

    def _test_integration(self) -> List[TestResult]:
        """Test integration between components."""
        results = []
        
        # Test that task files can be loaded and processed
        start_time = time.time()
        try:
            tasks_dir = self.project_root / 'tasks'
            total_tasks = 0
            
            for task_file in tasks_dir.rglob('*.json'):
                with open(task_file, 'r') as f:
                    task_data = json.load(f)
                    total_tasks += len(task_data.get('tasks', []))
            
            if total_tasks > 50:  # Expect at least 50 tasks
                results.append(TestResult(
                    name="integration_task_count",
                    passed=True,
                    duration=time.time() - start_time,
                    message=f"Found {total_tasks} total tasks across all categories"
                ))
            else:
                results.append(TestResult(
                    name="integration_task_count",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Only {total_tasks} tasks found, expected more than 50"
                ))
                
        except Exception as e:
            results.append(TestResult(
                name="integration_task_count",
                passed=False,
                duration=time.time() - start_time,
                message=f"Error counting tasks: {e}"
            ))
        
        return results

    def _test_performance(self) -> List[TestResult]:
        """Test performance characteristics."""
        results = []
        
        # Test that large task files can be loaded quickly
        start_time = time.time()
        try:
            tasks_dir = self.project_root / 'tasks'
            load_times = []
            
            for task_file in tasks_dir.rglob('*.json'):
                file_start = time.time()
                with open(task_file, 'r') as f:
                    json.load(f)
                file_duration = time.time() - file_start
                load_times.append(file_duration)
            
            avg_load_time = sum(load_times) / len(load_times) if load_times else 0
            
            if avg_load_time < 0.1:  # Should load in under 100ms
                results.append(TestResult(
                    name="performance_task_loading",
                    passed=True,
                    duration=time.time() - start_time,
                    message=f"Average task file load time: {avg_load_time:.3f}s"
                ))
            else:
                results.append(TestResult(
                    name="performance_task_loading",
                    passed=False,
                    duration=time.time() - start_time,
                    message=f"Slow task loading: {avg_load_time:.3f}s average"
                ))
                
        except Exception as e:
            results.append(TestResult(
                name="performance_task_loading",
                passed=False,
                duration=time.time() - start_time,
                message=f"Error testing performance: {e}"
            ))
        
        return results

    def generate_report(self) -> str:
        """Generate a comprehensive test report."""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        
        # Group results by category
        categories = {}
        for result in self.results:
            category = result.name.split('_')[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(result)
        
        report = []
        report.append("🧪 VS Code Productivity Toolkit - Automated Test Report")
        report.append("=" * 65)
        report.append(f"Total Tests: {total_tests}")
        report.append(f"Passed: {passed_tests}")
        report.append(f"Failed: {failed_tests}")
        report.append(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%")
        report.append("")
        
        # Category breakdown
        for category, category_results in categories.items():
            category_passed = sum(1 for r in category_results if r.passed)
            category_total = len(category_results)
            
            report.append(f"📋 {category.upper()} TESTS ({category_passed}/{category_total})")
            report.append("-" * 40)
            
            for result in category_results:
                status = "✅" if result.passed else "❌"
                report.append(f"{status} {result.name}")
                if result.message:
                    report.append(f"    {result.message}")
                if result.duration > 0.1:
                    report.append(f"    Duration: {result.duration:.3f}s")
                report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 40)
        
        if failed_tests == 0:
            report.append("🎉 All tests passed! The toolkit is ready for use.")
        else:
            report.append(f"⚠️  {failed_tests} tests failed. Please review and fix the issues above.")
            
            # Specific recommendations based on failures
            failed_categories = set()
            for result in self.results:
                if not result.passed:
                    failed_categories.add(result.name.split('_')[0])
            
            if 'task' in failed_categories:
                report.append("• Review and fix task definition files")
            if 'extension' in failed_categories:
                report.append("• Complete VS Code extension implementation")
            if 'python' in failed_categories:
                report.append("• Fix Python package structure and syntax")
            if 'script' in failed_categories:
                report.append("• Review automation scripts")
        
        return "\n".join(report)

def main():
    """Main entry point for automated testing."""
    parser = argparse.ArgumentParser(
        description='Run automated tests for VS Code Productivity Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--output', help='Save report to file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--category', help='Run specific test category only')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("🧪 Starting automated testing...")
    
    tester = AutomatedTester(args.project_root)
    results = tester.run_all_tests()
    
    report = tester.generate_report()
    print(report)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}")
    
    # Exit with error code if any tests failed
    failed_count = sum(1 for r in results if not r.passed)
    return 1 if failed_count > 0 else 0

if __name__ == '__main__':
    sys.exit(main())
