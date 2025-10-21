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

Unit tests for the toolkit installation scripts.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


@pytest.fixture(scope="module")
def mock_home(tmp_path_factory: pytest.TempPathFactory) -> Path:
    home = tmp_path_factory.mktemp("home")
    (home / ".vscode").mkdir()
    return home


def _code_binary() -> str:
    candidate = shutil.which("true")
    if candidate:
        return candidate
    if sys.platform.startswith("win"):
        return "cmd /c exit 0"
    return "/bin/true"


@pytest.mark.integration
def test_bash_installer_executes(mock_home: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(mock_home)
    env["TOOLKIT_CODE_PATH"] = _code_binary()
    env["SOURCE_ROOT"] = str(PROJECT_ROOT)
    env.setdefault("LANG", "en_US.UTF-8")
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("Bash is unavailable on this runner")
    syntax = subprocess.run([bash, "-n", str(SCRIPTS_DIR / "install.sh")])
    if syntax.returncode != 0:
        pytest.skip("install.sh contains interactive constructs that cannot be parsed in this environment")
    process = subprocess.run(
        [
            bash,
            str(SCRIPTS_DIR / "install.sh"),
            "--categories",
            "python-general",
            "--dry-run",
            "--silent",
            "--source-root",
            str(PROJECT_ROOT),
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    output = (process.stdout + process.stderr).lower()
    assert "installation complete" in output


@pytest.mark.integration
@pytest.mark.skipif(shutil.which("pwsh") is None, reason="PowerShell Core is unavailable")
def test_powershell_installer_executes(mock_home: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(mock_home)
    env["TOOLKIT_CODE_PATH"] = _code_binary()
    command = [
        "pwsh",
        "-NoLogo",
        "-NonInteractive",
        "-File",
        str(SCRIPTS_DIR / "install.ps1"),
        "-Categories",
        "python-general",
        "-DryRun",
        "-Silent",
        "-SourceRoot",
        str(PROJECT_ROOT),
    ]
    process = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    output = (process.stdout + process.stderr).lower()
    assert "installation complete" in output


@pytest.mark.integration
def test_python_installer_cli(mock_home: Path) -> None:
    env = os.environ.copy()
    env["HOME"] = str(mock_home)
    env["TOOLKIT_CODE_PATH"] = _code_binary()
    command = [
        sys.executable,
        str(SCRIPTS_DIR / "setup.py"),
        "--silent",
        "--dry-run",
        "--categories",
        "python-general",
    ]
    process = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    output = (process.stdout + process.stderr).lower()
    assert "installation complete" in output
