#!/usr/bin/env python3
"""
VS Code Productivity Toolkit - Bulk Installation Script

Installs productivity tasks across multiple projects in batch operations.
Useful for teams or when setting up multiple development environments.

Author: Diogo Ribeiro (dfr@esmad.ipp.pt)
License: MIT
"""

import os
import sys
import json
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse
import concurrent.futures
import logging
from dataclasses import dataclass
import subprocess
import time

# Import the bootstrap components
sys.path.append(str(Path(__file__).parent))
from bootstrap_workspace import ProjectDetector, TaskInstaller


@dataclass
class BulkInstallResult:
    """Result of bulk installation operation."""

    path: str
    success: bool
    detected_types: List[str]
    installed_tasks: int
    error: Optional[str] = None
    duration: float = 0.0


class BulkInstaller:
    """Handles bulk installation of VS Code tasks across multiple projects."""

    def __init__(
        self, max_workers: int = 4, task_source: str = "local", dry_run: bool = False
    ):
        self.max_workers = max_workers
        self.task_source = task_source
        self.dry_run = dry_run
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(), logging.FileHandler("bulk_install.log")],
        )
        return logging.getLogger(__name__)

    def find_projects(
        self, base_path: str, patterns: List[str], max_depth: int = 3
    ) -> List[str]:
        """Find project directories based on patterns."""
        projects = []
        base_path = Path(base_path).resolve()

        self.logger.info(f"Searching for projects in: {base_path}")

        if patterns:
            # Use provided glob patterns
            for pattern in patterns:
                full_pattern = str(base_path / pattern)
                matched_paths = glob.glob(full_pattern, recursive=True)
                for path in matched_paths:
                    if Path(path).is_dir():
                        projects.append(str(Path(path).resolve()))
        else:
            # Auto-discover projects by looking for common indicators
            indicators = [
                "package.json",
                "requirements.txt",
                "setup.py",
                "pyproject.toml",
                "Dockerfile",
                ".git",
                "go.mod",
                "Cargo.toml",
                "pom.xml",
                "build.gradle",
            ]

            for root, dirs, files in os.walk(base_path):
                # Limit search depth
                current_depth = root[len(str(base_path)) :].count(os.sep)
                if current_depth >= max_depth:
                    dirs[:] = []  # Don't go deeper
                    continue

                # Skip common non-project directories
                dirs[:] = [
                    d
                    for d in dirs
                    if d
                    not in {
                        "node_modules",
                        ".git",
                        "__pycache__",
                        ".venv",
                        "venv",
                        "dist",
                        "build",
                        ".next",
                        "target",
                        "out",
                    }
                ]

                # Check if this directory contains project indicators
                if any(
                    indicator in files or indicator in dirs for indicator in indicators
                ):
                    projects.append(root)

        # Remove duplicates and sort
        projects = sorted(list(set(projects)))
        self.logger.info(f"Found {len(projects)} potential projects")

        return projects

    def install_project_tasks(self, project_path: str) -> BulkInstallResult:
        """Install tasks for a single project."""
        start_time = time.time()

        try:
            self.logger.info(f"Processing project: {project_path}")

            # Detect project types
            detector = ProjectDetector(project_path)
            detected_projects = detector.detect_project_types()

            if not detected_projects:
                return BulkInstallResult(
                    path=project_path,
                    success=False,
                    detected_types=[],
                    installed_tasks=0,
                    error="No project types detected",
                    duration=time.time() - start_time,
                )

            detected_types = [p.type for p in detected_projects]
            self.logger.info(f"Detected types: {detected_types}")

            if self.dry_run:
                return BulkInstallResult(
                    path=project_path,
                    success=True,
                    detected_types=detected_types,
                    installed_tasks=0,  # Would be calculated in real run
                    duration=time.time() - start_time,
                )

            # Install tasks
            installer = TaskInstaller(project_path)
            installer.install_tasks_for_types(detected_types, self.task_source)

            # Count installed tasks (rough estimate)
            vscode_tasks_file = Path(project_path) / ".vscode" / "tasks.json"
            installed_count = 0
            if vscode_tasks_file.exists():
                try:
                    with open(vscode_tasks_file, "r") as f:
                        tasks_data = json.load(f)
                        installed_count = len(tasks_data.get("tasks", []))
                except Exception as e:
                    self.logger.warning(
                        f"Could not count tasks in {vscode_tasks_file}: {e}"
                    )

            return BulkInstallResult(
                path=project_path,
                success=True,
                detected_types=detected_types,
                installed_tasks=installed_count,
                duration=time.time() - start_time,
            )

        except Exception as e:
            self.logger.error(f"Error processing {project_path}: {e}")
            return BulkInstallResult(
                path=project_path,
                success=False,
                detected_types=[],
                installed_tasks=0,
                error=str(e),
                duration=time.time() - start_time,
            )

    def install_bulk(self, projects: List[str]) -> List[BulkInstallResult]:
        """Install tasks for multiple projects in parallel."""
        results = []

        self.logger.info(f"Starting bulk installation for {len(projects)} projects")
        self.logger.info(f"Using {self.max_workers} worker threads")

        if self.dry_run:
            self.logger.info("DRY RUN MODE - No tasks will be actually installed")

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            future_to_project = {
                executor.submit(self.install_project_tasks, project): project
                for project in projects
            }

            for future in concurrent.futures.as_completed(future_to_project):
                project = future_to_project[future]
                try:
                    result = future.result()
                    results.append(result)

                    if result.success:
                        self.logger.info(
                            f"✓ {project}: {len(result.detected_types)} types, "
                            f"{result.installed_tasks} tasks, "
                            f"{result.duration:.2f}s"
                        )
                    else:
                        self.logger.error(f"✗ {project}: {result.error}")

                except Exception as e:
                    self.logger.error(f"✗ {project}: Unexpected error: {e}")
                    results.append(
                        BulkInstallResult(
                            path=project,
                            success=False,
                            detected_types=[],
                            installed_tasks=0,
                            error=str(e),
                        )
                    )

        return results

    def generate_report(self, results: List[BulkInstallResult]) -> Dict[str, Any]:
        """Generate a comprehensive installation report."""
        total_projects = len(results)
        successful = sum(1 for r in results if r.success)
        failed = total_projects - successful
        total_tasks = sum(r.installed_tasks for r in results)
        total_duration = sum(r.duration for r in results)

        # Categorize by project type
        type_stats = {}
        for result in results:
            for ptype in result.detected_types:
                if ptype not in type_stats:
                    type_stats[ptype] = {"count": 0, "tasks": 0}
                type_stats[ptype]["count"] += 1
                type_stats[ptype]["tasks"] += result.installed_tasks

        # Error analysis
        error_types = {}
        for result in results:
            if not result.success and result.error:
                error_key = result.error.split(":")[0]  # Get error type
                error_types[error_key] = error_types.get(error_key, 0) + 1

        report = {
            "summary": {
                "total_projects": total_projects,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful / total_projects) * 100:.1f}%"
                if total_projects > 0
                else "0%",
                "total_tasks_installed": total_tasks,
                "total_duration": f"{total_duration:.2f}s",
                "average_duration": f"{total_duration / total_projects:.2f}s"
                if total_projects > 0
                else "0s",
            },
            "project_types": type_stats,
            "error_analysis": error_types,
            "detailed_results": [
                {
                    "path": r.path,
                    "success": r.success,
                    "detected_types": r.detected_types,
                    "installed_tasks": r.installed_tasks,
                    "duration": f"{r.duration:.2f}s",
                    "error": r.error,
                }
                for r in results
            ],
        }

        return report

    def save_report(self, report: Dict[str, Any], output_file: str):
        """Save the installation report to a file."""
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        self.logger.info(f"Report saved to: {output_file}")


def main():
    """Main entry point for bulk installation script."""
    parser = argparse.ArgumentParser(
        description="Bulk install VS Code productivity tasks across multiple projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install tasks for all projects in a directory
  python bulk-install.py /path/to/projects

  # Install with specific patterns
  python bulk-install.py /path/to/projects --patterns "*/frontend" "*/backend" 

  # Dry run to see what would be installed
  python bulk-install.py /path/to/projects --dry-run

  # Use specific project types only
  python bulk-install.py /path/to/projects --types python javascript

  # Generate detailed report
  python bulk-install.py /path/to/projects --report bulk_install_report.json
        """,
    )

    parser.add_argument("base_path", help="Base directory to search for projects")
    parser.add_argument(
        "--patterns", nargs="+", help="Glob patterns for finding projects"
    )
    parser.add_argument(
        "--types", nargs="+", help="Specific project types to install (if detected)"
    )
    parser.add_argument(
        "--max-depth", type=int, default=3, help="Maximum search depth (default: 3)"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=4,
        help="Maximum parallel workers (default: 4)",
    )
    parser.add_argument(
        "--task-source", default="local", help="Task source: local or URL"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without installing",
    )
    parser.add_argument("--report", help="Save detailed report to JSON file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print("🚀 VS Code Productivity Toolkit - Bulk Installer")
    print("=" * 55)

    # Validate base path
    if not Path(args.base_path).exists():
        print(f"❌ Base path does not exist: {args.base_path}")
        return 1

    # Initialize bulk installer
    installer = BulkInstaller(
        max_workers=args.max_workers, task_source=args.task_source, dry_run=args.dry_run
    )

    # Find projects
    projects = installer.find_projects(
        args.base_path, args.patterns or [], args.max_depth
    )

    if not projects:
        print("❌ No projects found matching criteria")
        return 1

    print(f"📋 Found {len(projects)} projects to process")

    # Confirm before proceeding
    if not args.dry_run:
        response = input("Continue with installation? (y/N): ")
        if response.lower() != "y":
            print("Installation cancelled")
            return 0

    # Install tasks
    start_time = time.time()
    results = installer.install_bulk(projects)
    total_time = time.time() - start_time

    # Generate and display report
    report = installer.generate_report(results)

    print("\n" + "=" * 55)
    print("📊 INSTALLATION REPORT")
    print("=" * 55)
    print(f"Total Projects: {report['summary']['total_projects']}")
    print(f"Successful: {report['summary']['successful']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"Success Rate: {report['summary']['success_rate']}")
    print(f"Total Tasks Installed: {report['summary']['total_tasks_installed']}")
    print(f"Total Duration: {total_time:.2f}s")

    if report["project_types"]:
        print("\n📈 Project Types:")
        for ptype, stats in report["project_types"].items():
            print(f"  {ptype}: {stats['count']} projects, {stats['tasks']} tasks")

    if report["error_analysis"]:
        print("\n❌ Errors:")
        for error, count in report["error_analysis"].items():
            print(f"  {error}: {count} occurrences")

    # Save detailed report if requested
    if args.report:
        installer.save_report(report, args.report)

    # Exit with appropriate code
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
