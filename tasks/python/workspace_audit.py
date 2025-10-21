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

Workspace auditing utilities for VS Code environments.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, NamedTuple

from toolkit.logging import get_logger


class ConfigFindings(NamedTuple):
    """Structured findings related to workspace configuration files."""

    settingsPresent: bool
    keybindingsPresent: bool
    missingFiles: List[str]
    extensions: List[str]


class WorkspaceAuditor:
    """Audit a VS Code workspace and provide actionable insights."""

    def __init__(self, *, workspace_path: Path, recommended_extensions: List[str]) -> None:
        if not workspace_path.exists() or not workspace_path.is_dir():
            raise ValueError("Workspace path is invalid. Provide an existing directory.")
        self._workspace_path = workspace_path
        self._recommended_extensions = recommended_extensions
        self._logger = get_logger(self.__class__.__name__)

    def run(self) -> Dict[str, object]:
        """Execute the workspace audit."""

        self._logger.info(
            "Starting workspace audit", extra={"extra": {"workspace": str(self._workspace_path)}}
        )
        config_findings = self._inspect_vscode_config()
        extension_findings = self._compare_extensions(config_findings.extensions)
        report = {
            "workspace": str(self._workspace_path),
            "configFindings": config_findings._asdict(),
            "extensionCompliance": extension_findings,
        }
        self._logger.info(
            "Workspace audit completed", extra={"extra": {"summary": report}}
        )
        return report

    def _inspect_vscode_config(self) -> ConfigFindings:
        settings_file = self._workspace_path / ".vscode" / "settings.json"
        keybindings_file = self._workspace_path / ".vscode" / "keybindings.json"

        settings_status = settings_file.exists()
        keybindings_status = keybindings_file.exists()

        missing_files: List[str] = []
        if not settings_status:
            missing_files.append(str(settings_file))
        if not keybindings_status:
            missing_files.append(str(keybindings_file))

        extensions = self._load_extensions()

        return ConfigFindings(
            settingsPresent=settings_status,
            keybindingsPresent=keybindings_status,
            missingFiles=missing_files,
            extensions=extensions,
        )

    def _load_extensions(self) -> List[str]:
        extensions_file = self._workspace_path / ".vscode" / "extensions.json"
        if not extensions_file.exists():
            self._logger.warning(
                "extensions.json not found", extra={"extra": {"path": str(extensions_file)}}
            )
            return []
        try:
            with extensions_file.open("r", encoding="utf-8") as handle:
                content = json.load(handle)
        except (json.JSONDecodeError, OSError) as error:
            self._logger.error(
                "Failed to parse extensions.json",
                extra={"extra": {"path": str(extensions_file), "error": str(error)}},
            )
            return []
        recommendations = content.get("recommendations", [])
        if not isinstance(recommendations, list):
            self._logger.warning(
                "Invalid recommendations format",
                extra={"extra": {"path": str(extensions_file)}},
            )
            return []
        return [str(extension) for extension in recommendations]

    def _compare_extensions(self, workspace_extensions: List[str]) -> Dict[str, List[str]]:
        missing = sorted(
            extension
            for extension in self._recommended_extensions
            if extension not in workspace_extensions
        )
        unexpected = sorted(
            extension
            for extension in workspace_extensions
            if extension not in self._recommended_extensions
        )
        return {
            "recommendedMissing": missing,
            "unexpected": unexpected,
        }
