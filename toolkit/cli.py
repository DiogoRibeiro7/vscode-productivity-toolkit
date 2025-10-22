"""
# File Location: /toolkit/
MIT License
Copyright (c) 2025 Diogo Ribeiro

Command-line interface for the VS Code Productivity Toolkit.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

from .detector import ProjectDetector
from .installer import TaskInstaller
from .utils import setup_logging, validate_workspace, TaskCategory

# Configure logging
logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="vscode-toolkit",
        description="VS Code Productivity Toolkit - Enterprise automation for developers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect project and install recommended tasks
  vscode-toolkit install --auto-detect
  
  # Install specific task categories
  vscode-toolkit install --categories python-general,docker,git
  
  # Detect project type without installing
  vscode-toolkit detect --workspace .
  
  # Export current configuration
  vscode-toolkit export --output my-config.json
  
  # Import team configuration
  vscode-toolkit import --config team-config.json
  
  # Validate custom tasks
  vscode-toolkit validate --path ./custom-tasks/
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="vscode-toolkit 1.0.0",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=0,
        help="Increase verbosity (use -v, -vv, or -vvv)",
    )

    parser.add_argument(
        "--workspace", "-w",
        type=Path,
        default=Path.cwd(),
        help="Path to workspace directory (default: current directory)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    install_parser = subparsers.add_parser(
        "install",
        help="Install productivity tasks",
    )
    install_group = install_parser.add_mutually_exclusive_group(required=True)
    install_group.add_argument(
        "--auto-detect",
        action="store_true",
        help="Auto-detect project type and install recommended tasks",
    )
    install_group.add_argument(
        "--categories",
        type=str,
        help="Comma-separated list of task categories to install",
    )
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="Force installation even if tasks.json exists",
    )
    install_parser.add_argument(
        "--backup",
        action="store_true",
        default=True,
        help="Create backup before installation (default: True)",
    )

    # Detect command
    detect_parser = subparsers.add_parser(
        "detect",
        help="Detect project type and suggest tasks",
    )
    detect_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )

    # Export command
    export_parser = subparsers.add_parser(
        "export",
        help="Export current task configuration",
    )
    export_parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output file path for exported configuration",
    )
    export_parser.add_argument(
        "--include-settings",
        action="store_true",
        help="Include VS Code settings in export",
    )

    # Import command
    import_parser = subparsers.add_parser(
        "import",
        help="Import task configuration",
    )
    import_parser.add_argument(
        "--config", "-c",
        type=Path,
        required=True,
        help="Configuration file to import",
    )
    import_parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge with existing configuration",
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate task definitions",
    )
    validate_parser.add_argument(
        "--path", "-p",
        type=Path,
        help="Path to task definitions (default: current workspace)",
    )

    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List available task categories",
    )
    list_parser.add_argument(
        "--installed",
        action="store_true",
        help="Show only installed tasks",
    )

    # Clean command
    clean_parser = subparsers.add_parser(
        "clean",
        help="Clean up task configurations",
    )
    clean_parser.add_argument(
        "--backup-days",
        type=int,
        default=30,
        help="Remove backups older than N days (default: 30)",
    )

    return parser


def cmd_install(args: argparse.Namespace) -> int:
    """Handle the install command."""
    try:
        workspace = validate_workspace(args.workspace)
        installer = TaskInstaller(workspace)

        if args.auto_detect:
            logger.info("Auto-detecting project type...")
            detector = ProjectDetector()
            detection_result = detector.detect_project_type(workspace)
            
            if not detection_result.detected_types:
                logger.warning("No specific project type detected. Use --categories to install manually.")
                return 1

            categories = detector.suggest_task_categories(detection_result)
            logger.info(f"Detected project types: {', '.join(detection_result.detected_types)}")
            logger.info(f"Recommended categories: {', '.join(categories)}")

        else:
            categories = [cat.strip() for cat in args.categories.split(",")]
            logger.info(f"Installing categories: {', '.join(categories)}")

        # Validate categories
        for category in categories:
            if not TaskCategory.is_valid(category):
                logger.error(f"Invalid task category: {category}")
                return 1

        # Install tasks
        installer.install_task_categories(
            categories,
            force=args.force,
            create_backup=args.backup
        )

        logger.info("✅ Task installation completed successfully!")
        return 0

    except Exception as e:
        logger.error(f"Installation failed: {e}")
        return 1


def cmd_detect(args: argparse.Namespace) -> int:
    """Handle the detect command."""
    try:
        workspace = validate_workspace(args.workspace)
        detector = ProjectDetector()
        
        result = detector.detect_project_type(workspace)
        suggestions = detector.suggest_task_categories(result)

        if args.json:
            output = {
                "workspace": str(workspace),
                "detected_types": result.detected_types,
                "confidence": result.confidence,
                "evidence": result.evidence,
                "suggested_categories": suggestions,
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"Workspace: {workspace}")
            print(f"Detected project types: {', '.join(result.detected_types) or 'None'}")
            
            if result.detected_types:
                print("\nConfidence scores:")
                for proj_type, confidence in result.confidence.items():
                    print(f"  {proj_type}: {confidence:.1%}")
                
                print(f"\nSuggested task categories: {', '.join(suggestions)}")

        return 0

    except Exception as e:
        logger.error(f"Detection failed: {e}")
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Set up logging
    log_level = max(1, 3 - args.verbose) * 10  # 30=WARNING, 20=INFO, 10=DEBUG
    setup_logging(level=log_level)

    if not args.command:
        parser.print_help()
        return 1

    # Route to command handlers
    command_handlers = {
        "install": cmd_install,
        "detect": cmd_detect,
    }

    handler = command_handlers.get(args.command)
    if not handler:
        logger.error(f"Unknown command: {args.command}")
        return 1

    try:
        return handler(args)
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose >= 2:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
