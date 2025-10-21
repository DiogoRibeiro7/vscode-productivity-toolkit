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

Unit tests for the toolkit CLI.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from toolkit.cli import (  # noqa: E402
    auditWorkspace,
    buildParser,
    configureWorkspace,
    loadExtensions,
)


def test_load_extensions(tmp_path: Path) -> None:
    extensions_file = tmp_path / "extensions.json"
    extensions_file.write_text(
        json.dumps({"recommendations": ["example.extension", 123]}),
        encoding="utf-8",
    )
    extensions = loadExtensions(extensions_file)
    assert extensions == ["example.extension", "123"]


def test_audit_workspace_generates_report(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    workspace = tmp_path / "workspace"
    vscode_dir = workspace / ".vscode"
    vscode_dir.mkdir(parents=True)
    (vscode_dir / "extensions.json").write_text(
        json.dumps({"recommendations": ["ms-python.python"]}),
        encoding="utf-8",
    )

    args = argparse.Namespace(
        workspace=str(workspace),
        extensions=str(vscode_dir / "extensions.json"),
        output=None,
    )
    auditWorkspace(args)
    captured = json.loads(capsys.readouterr().out)
    assert captured["workspace"] == str(workspace)
    assert captured["configFindings"]["settingsPresent"] is False


def test_configure_workspace_exports_files(tmp_path: Path) -> None:
    destination = tmp_path / "exported"
    args = argparse.Namespace(output=str(destination), force=True)
    configureWorkspace(args)
    expected_files = {"settings.json", "keybindings.json", "extensions.json"}
    assert expected_files.issubset({file.name for file in destination.iterdir()})


def test_build_parser_supports_commands() -> None:
    parser = buildParser()
    args = parser.parse_args(
        [
            "--log-level",
            "DEBUG",
            "audit",
            "--workspace",
            "/tmp",
        ]
    )
    assert args.command == "audit"
