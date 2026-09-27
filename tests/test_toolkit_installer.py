"""Integration tests for installing tasks over existing VS Code configuration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from toolkit.installer import TaskInstaller
from toolkit.utils import ValidationError


def test_cli_install_preserves_shell_installer_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """CLI installs should retain source metadata written by shell installers."""
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    tasks_path = vscode_dir / "tasks.json"
    source_metadata = {"license": "MIT", "description": "Shell installer source"}
    tasks_path.write_text(
        json.dumps(
            {
                "version": "2.0.0",
                "tasks": [{"label": "existing", "type": "shell", "command": "echo old"}],
                "_toolkitMetadata": [source_metadata],
            }
        ),
        encoding="utf-8",
    )

    installer = TaskInstaller(tmp_path)

    def download_category(category: str) -> Dict[str, Any]:
        assert category == "python-general"
        return {
            "tasks": [{"label": "new", "type": "shell", "command": "echo new"}]
        }

    monkeypatch.setattr(installer, "_download_task_category", download_category)

    # Reinstalling the same category should keep both the tasks and metadata stable.
    installer.install_task_categories(["python-general"], create_backup=False)
    installer.install_task_categories(["python-general"], create_backup=False)

    result = json.loads(tasks_path.read_text(encoding="utf-8"))
    assert [task["label"] for task in result["tasks"]] == ["existing", "new"]

    metadata = result["_toolkitMetadata"]
    assert isinstance(metadata, list)
    assert metadata[0] == source_metadata
    assert len(metadata) == 2
    assert metadata[1]["installedCategories"] == ["python-general"]
    assert metadata[1]["lastUpdated"]


@pytest.mark.parametrize(
    ("existing_content", "error"),
    [
        ('{"version": "2.0.0", "tasks": [', "Cannot read existing tasks.json"),
        ("[]", "must be a JSON object"),
    ],
)
def test_install_preserves_invalid_existing_tasks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    existing_content: str,
    error: str,
) -> None:
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    tasks_path = vscode_dir / "tasks.json"
    tasks_path.write_text(existing_content, encoding="utf-8")
    installer = TaskInstaller(tmp_path)

    monkeypatch.setattr(
        installer,
        "_download_task_category",
        lambda category: {"tasks": [{"label": "new", "command": "echo new"}]},
    )

    with pytest.raises(ValidationError, match=error):
        installer.install_task_categories(["python-general"], create_backup=False)

    assert tasks_path.read_text(encoding="utf-8") == existing_content


def test_failed_write_preserves_existing_tasks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()
    tasks_path = vscode_dir / "tasks.json"
    original = '{"version": "2.0.0", "tasks": [{"label": "existing"}]}'
    tasks_path.write_text(original, encoding="utf-8")
    installer = TaskInstaller(tmp_path)

    def fail_after_partial_write(_tasks: Any, stream: Any, **_options: Any) -> None:
        stream.write('{"tasks": [')
        raise OSError("simulated write failure")

    monkeypatch.setattr("toolkit.installer.json.dump", fail_after_partial_write)

    with pytest.raises(ValidationError, match="Failed to write tasks.json"):
        installer._write_tasks_file({"version": "2.0.0", "tasks": []})

    assert tasks_path.read_text(encoding="utf-8") == original
    assert {path.name for path in vscode_dir.iterdir()} == {"tasks.json"}
