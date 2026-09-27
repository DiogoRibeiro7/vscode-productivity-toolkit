"""Tests for the public command-line interface."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from toolkit import cli


def test_create_parser_supports_install_auto_detect(tmp_path: Path) -> None:
    parser = cli.create_parser()
    args = parser.parse_args(
        ["--workspace", str(tmp_path), "install", "--auto-detect"]
    )

    assert args.command == "install"
    assert args.auto_detect is True
    assert args.workspace == tmp_path


def test_create_parser_supports_detect_json(tmp_path: Path) -> None:
    parser = cli.create_parser()
    args = parser.parse_args(["--workspace", str(tmp_path), "detect", "--json"])

    assert args.command == "detect"
    assert args.json is True


def test_help_only_advertises_implemented_commands() -> None:
    help_text = cli.create_parser().format_help()

    assert "{install,detect}" in help_text
    assert "vscode-toolkit --workspace . detect" in help_text
    assert "vscode-toolkit export" not in help_text


def test_cmd_detect_emits_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    class DetectorStub:
        def detect_project_type(self, workspace: Path) -> SimpleNamespace:
            assert workspace == tmp_path
            return SimpleNamespace(
                detected_types=["Python"],
                confidence={"Python": 0.9},
                evidence={"Python": ["pyproject.toml"]},
            )

        def suggest_task_categories(self, result: SimpleNamespace) -> list[str]:
            assert result.detected_types == ["Python"]
            return ["python-general"]

    monkeypatch.setattr(cli, "validate_workspace", lambda _: tmp_path)
    monkeypatch.setattr(cli, "ProjectDetector", DetectorStub)

    args = SimpleNamespace(workspace=tmp_path, json=True)
    assert cli.cmd_detect(args) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["workspace"] == str(tmp_path)
    assert payload["detected_types"] == ["Python"]
    assert payload["suggested_categories"] == ["python-general"]


def test_main_without_command_returns_error() -> None:
    assert cli.main([]) == 1
