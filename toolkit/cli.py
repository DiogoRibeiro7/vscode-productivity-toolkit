"""
MIT License
Copyright (c) 2025 Diogo Ribeiro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Command-line interface for the vscode-productivity-toolkit.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, List

from tasks.python.workspace_audit import WorkspaceAuditor
from toolkit.logging import configure_logging, get_logger

DEFAULT_TIMEOUT_SECONDS = 25


def loadExtensions(extensions_file: Path) -> List[str]:
    """Load extension recommendations from a JSON file."""

    if not extensions_file.exists():
        raise FileNotFoundError(f"Extensions file not found: {extensions_file}")
    with extensions_file.open("r", encoding="utf-8") as handle:
        content = json.load(handle)
    recommendations = content.get("recommendations", [])
    if not isinstance(recommendations, list):
        raise ValueError("The recommendations field must be an array.")
    return [str(extension) for extension in recommendations]


def auditWorkspace(args: argparse.Namespace) -> None:
    """Run the workspace auditor and optionally persist the report."""

    logger = get_logger("toolkit.audit")
    workspace_path = Path(args.workspace).expanduser().resolve()
    extensions_file = Path(args.extensions).expanduser().resolve()
    try:
        recommended_extensions = loadExtensions(extensions_file)
    except (OSError, ValueError) as error:
        logger.error("Failed to load extensions", extra={"extra": {"error": str(error)}})
        raise

    auditor = WorkspaceAuditor(
        workspace_path=workspace_path, recommended_extensions=recommended_extensions
    )
    report = auditor.run()
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
        logger.info("Audit report saved", extra={"extra": {"path": str(output_path)}})
    else:
        print(json.dumps(report, indent=2))


def configureWorkspace(args: argparse.Namespace) -> None:
    """Export curated configuration files to a destination directory."""

    logger = get_logger("toolkit.configure")
    destination = Path(args.output).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    config_dir = Path(__file__).resolve().parents[1] / "settings"
    files_to_copy = [
        config_dir / "settings.json",
        config_dir / "keybindings.json",
        config_dir / "extensions.json",
    ]
    for file_path in files_to_copy:
        if not file_path.exists():
            logger.error(
                "Configuration file missing", extra={"extra": {"path": str(file_path)}}
            )
            raise FileNotFoundError(f"Configuration file missing: {file_path}")
        target_path = destination / file_path.name
        if target_path.exists() and not args.force:
            logger.warning(
                "File already exists", extra={"extra": {"path": str(target_path)}}
            )
            continue
        try:
            shutil.copy2(file_path, target_path)
        except OSError as error:
            logger.error(
                "Failed to copy configuration",
                extra={"extra": {"source": str(file_path), "target": str(target_path)}},
            )
            raise error
        logger.info(
            "Configuration exported",
            extra={"extra": {"source": str(file_path), "target": str(target_path)}},
        )


def manageExtensions(args: argparse.Namespace) -> None:
    """Install recommended extensions using the VS Code CLI."""

    logger = get_logger("toolkit.extensions")
    extensions_file = Path(args.extensions).expanduser().resolve()
    try:
        extensions = loadExtensions(extensions_file)
    except (OSError, ValueError) as error:
        logger.error("Failed to load extensions", extra={"extra": {"error": str(error)}})
        raise

    code_binary = Path(args.code_binary).expanduser() if args.code_binary else None
    command_base: List[str]
    if code_binary:
        command_base = [str(code_binary)]
    else:
        command_base = ["code"]

    for extension in extensions:
        command = command_base + ["--install-extension", extension]
        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )
            logger.info(
                "Extension installed", extra={"extra": {"extension": extension}}
            )
        except subprocess.CalledProcessError as error:
            logger.error(
                "Failed to install extension",
                extra={
                    "extra": {
                        "extension": extension,
                        "returncode": error.returncode,
                        "stderr": error.stderr.decode("utf-8", errors="ignore"),
                    }
                },
            )
            if not args.keep_going:
                raise
        except subprocess.TimeoutExpired:
            logger.error(
                "Timed out installing extension",
                extra={"extra": {"extension": extension}},
            )
            if not args.keep_going:
                raise


def buildParser() -> argparse.ArgumentParser:
    """Construct the argument parser for the CLI."""

    parser = argparse.ArgumentParser(
        prog="vscode-productivity-toolkit",
        description="Automation utilities for managing VS Code productivity workflows.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging verbosity (DEBUG, INFO, WARNING, ERROR).",
    )
    parser.add_argument(
        "--plain-logs",
        action="store_true",
        help="Use plain text logs instead of JSON output.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Audit a VS Code workspace.")
    audit_parser.add_argument("--workspace", required=True, help="Path to the workspace.")
    audit_parser.add_argument(
        "--extensions",
        default=str(Path(__file__).resolve().parents[1] / "settings" / "extensions.json"),
        help="Path to the recommended extensions file.",
    )
    audit_parser.add_argument(
        "--output",
        help="Optional path to save the audit report as JSON.",
    )
    audit_parser.set_defaults(func=auditWorkspace)

    configure_parser = subparsers.add_parser(
        "configure", help="Export curated configuration files."
    )
    configure_parser.add_argument(
        "--output", required=True, help="Destination directory for configuration files."
    )
    configure_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing configuration files.",
    )
    configure_parser.set_defaults(func=configureWorkspace)

    extensions_parser = subparsers.add_parser(
        "extensions", help="Install recommended extensions via the VS Code CLI."
    )
    extensions_parser.add_argument(
        "--extensions",
        default=str(Path(__file__).resolve().parents[1] / "settings" / "extensions.json"),
        help="Path to the recommended extensions file.",
    )
    extensions_parser.add_argument(
        "--code-binary",
        help="Path to the VS Code executable when it is not available on PATH.",
    )
    extensions_parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Continue installing extensions even if one fails.",
    )
    extensions_parser.set_defaults(func=manageExtensions)

    return parser


def main(argv: Iterable[str] | None = None) -> None:
    """Entry point for the CLI."""

    parser = buildParser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    configure_logging(level=args.log_level, use_json=not args.plain_logs)
    args.func(args)


if __name__ == "__main__":
    main()
