"""\
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

Validation tests for the Smart Task Detector extension manifest.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXTENSION_MANIFEST = PROJECT_ROOT / "extensions" / "smart-task-detector" / "package.json"


def test_extension_manifest_contains_commands() -> None:
    manifest = json.loads(EXTENSION_MANIFEST.read_text(encoding="utf-8"))
    contributes = manifest.get("contributes", {})
    commands = contributes.get("commands", [])
    assert commands, "Extension must declare at least one command"
    for command in commands:
        assert command.get("command"), "Command identifier is required"
        assert command.get("title"), "Command title is required"


def test_extension_activation_events_cover_supported_languages() -> None:
    manifest = json.loads(EXTENSION_MANIFEST.read_text(encoding="utf-8"))
    activation_events = manifest.get("activationEvents", [])
    expected_events = {"onStartupFinished", "workspaceContains:package.json", "workspaceContains:requirements.txt"}
    assert expected_events.issubset(set(activation_events)), "Missing activation events"
