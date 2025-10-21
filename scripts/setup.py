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
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import textwrap
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except Exception:  # pragma: no cover - tkinter may be unavailable in headless environments
    tk = None
    ttk = None
    messagebox = None

DEFAULT_SCHEMA = (
    "https://raw.githubusercontent.com/microsoft/vscode/master/src/vs/workbench/"
    "contrib/tasks/common/tasks.schema.json"
)

LOGGER = logging.getLogger("toolkit.setup")


def configure_logging(verbose: bool) -> None:
    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
            payload = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
                "level": record.levelname,
                "message": record.getMessage(),
            }
            if verbose:
                payload["module"] = record.module
                payload["line"] = record.lineno
            return json.dumps(payload)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    LOGGER.setLevel(logging.DEBUG if verbose else logging.INFO)
    LOGGER.handlers.clear()
    LOGGER.addHandler(handler)


@dataclass(frozen=True)
class TaskCategory:
    identifier: str
    label: str
    description: str
    relative_path: Path


class InstallationError(RuntimeError):
    """Raised when the installation process fails."""


class RollbackManager:
    def __init__(self) -> None:
        self._actions: List[Callable[[], None]] = []

    def register(self, action: Callable[[], None]) -> None:
        self._actions.append(action)

    def execute(self) -> None:
        while self._actions:
            action = self._actions.pop()
            try:
                action()
            except Exception as exc:  # pragma: no cover - rollback best effort
                LOGGER.warning("Rollback action failed: %s", exc)


class TaskInstaller:
    def __init__(
        self,
        project_root: Path,
        dry_run: bool = False,
        remote_base_url: Optional[str] = None,
        skip_extensions: bool = False,
    ) -> None:
        self.project_root = project_root
        self.dry_run = dry_run
        self.remote_base_url = remote_base_url.rstrip("/") if remote_base_url else None
        self.skip_extensions = skip_extensions
        self.settings_dir = project_root / "settings"
        self.rollback = RollbackManager()

    @property
    def source_root(self) -> Path:
        return self.project_root

    def available_categories(self) -> List[TaskCategory]:
        return [
            TaskCategory(
                "python-general",
                "Python – General",
                "Quality, packaging, docker, and git automation tasks.",
                Path("tasks/python/general.json"),
            ),
            TaskCategory(
                "python-data-science",
                "Python – Data Science",
                "Notebook conversion, profiling, and documentation workflows.",
                Path("tasks/python/data-science.json"),
            ),
            TaskCategory(
                "javascript-general",
                "JavaScript/TypeScript – General",
                "Linting, dependency hygiene, and documentation tasks.",
                Path("tasks/javascript/general.json"),
            ),
            TaskCategory(
                "javascript-node",
                "Node.js Services",
                "Express development, database migrations, and API testing.",
                Path("tasks/javascript/node.json"),
            ),
            TaskCategory(
                "javascript-react",
                "React Applications",
                "Component scaffolding, Storybook, bundle analysis, and PWA audits.",
                Path("tasks/javascript/react.json"),
            ),
        ]

    # region helper methods
    def _resolve_code_cli(self) -> Path:
        override = os.environ.get("TOOLKIT_CODE_PATH")
        if override:
            candidate = Path(override)
            if candidate.exists():
                return candidate
        for name in ("code", "code.cmd", "code.exe"):
            path = shutil.which(name)
            if path:
                return Path(path)
        raise InstallationError(
            "VS Code command line interface not found. Enable the 'code' command and retry."
        )

    def _ensure_vscode_dir(self) -> Path:
        vscode_dir = Path.home() / ".vscode"
        if not vscode_dir.exists() and not self.dry_run:
            LOGGER.debug("Creating VS Code configuration directory at %s", vscode_dir)
            vscode_dir.mkdir(parents=True, exist_ok=True)
        return vscode_dir

    def _download_content(self, category: TaskCategory) -> str:
        if not self.remote_base_url:
            file_path = self.project_root / category.relative_path
            if not file_path.exists():
                raise InstallationError(f"Task definition not found at {file_path}")
            LOGGER.debug("Loading task definition from %s", file_path)
            return file_path.read_text(encoding="utf-8")

        import urllib.request

        relative = str(category.relative_path).replace(os.sep, "/")
        url = f"{self.remote_base_url}/{relative}"
        LOGGER.info("Downloading task definition from %s", url)
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read().decode("utf-8")
        except Exception as exc:  # pragma: no cover - network path
            raise InstallationError(f"Failed to download {url}: {exc}") from exc
        return data

    def _load_json(self, content: str) -> Dict[str, object]:
        return json.loads(content)

    def _merge_tasks(
        self,
        existing: Optional[Dict[str, object]],
        additions: Sequence[Dict[str, object]],
    ) -> Dict[str, object]:
        schema = DEFAULT_SCHEMA
        version = "2.0.0"
        inputs: List[object] = []
        tasks: List[object] = []
        matchers: List[object] = []
        metadata: List[object] = []

        def ingest(config: Optional[Dict[str, object]]) -> None:
            nonlocal schema, version
            if not config:
                return
            schema = str(config.get("$schema", schema))
            version = str(config.get("version", version))

            def append_unique(destination: List[object], values: Iterable[object], key: str) -> None:
                seen: Set[str] = set()
                for existing_item in destination:
                    if isinstance(existing_item, dict) and key in existing_item:
                        seen.add(str(existing_item[key]))
                for item in values:
                    if isinstance(item, dict) and key in item:
                        identifier = str(item[key])
                        if identifier in seen:
                            continue
                        seen.add(identifier)
                    destination.append(item)

            append_unique(inputs, config.get("inputs", []) or [], "id")
            append_unique(tasks, config.get("tasks", []) or [], "label")
            append_unique(matchers, config.get("problemMatchers", []) or [], "name")

            raw_metadata = config.get("_toolkitMetadata") or config.get("_metadata")
            if raw_metadata:
                entries = raw_metadata if isinstance(raw_metadata, list) else [raw_metadata]
                serialized: Set[str] = {json.dumps(item, sort_keys=True) for item in metadata if isinstance(item, dict)}
                for entry in entries:
                    payload = entry if isinstance(entry, dict) else {"value": entry}
                    signature = json.dumps(payload, sort_keys=True)
                    if signature in serialized:
                        continue
                    serialized.add(signature)
                    metadata.append(payload)

        ingest(existing)
        for block in additions:
            ingest(block)

        result: Dict[str, object] = {"$schema": schema, "version": version}
        if inputs:
            result["inputs"] = inputs
        if tasks:
            result["tasks"] = tasks
        if matchers:
            result["problemMatchers"] = matchers
        if metadata:
            result["_toolkitMetadata"] = metadata
        return result

    def _write_json(self, path: Path, payload: Dict[str, object]) -> None:
        text = json.dumps(payload, indent=2)
        if self.dry_run:
            LOGGER.info("[Dry Run] Would write %s", path)
            return
        LOGGER.debug("Writing merged tasks to %s", path)
        path.write_text(text + "\n", encoding="utf-8")

    def _backup_file(self, source: Path) -> Optional[Path]:
        if not source.exists():
            return None
        backup = source.with_name(f"{source.name}.bak.{int(time.time())}")
        if not self.dry_run:
            shutil.copy2(source, backup)
        LOGGER.debug("Backed up %s to %s", source, backup)
        self.rollback.register(lambda: shutil.copy2(backup, source) if backup.exists() else None)
        return backup

    def _synchronize_file(self, source: Path, destination: Path) -> None:
        if not source.exists():
            LOGGER.debug("Skipping missing source %s", source)
            return
        if destination.exists():
            self._backup_file(destination)
        if self.dry_run:
            LOGGER.info("[Dry Run] Would copy %s to %s", source, destination)
        else:
            shutil.copy2(source, destination)
        LOGGER.info("Synchronized %s", destination)

    def _install_extensions(self, code_cli: Path, extensions_file: Path) -> None:
        if self.skip_extensions:
            LOGGER.info("Skipping extension installation as requested.")
            return
        if not extensions_file.exists():
            LOGGER.warning("Extensions configuration not found at %s", extensions_file)
            return
        recommendations = json.loads(extensions_file.read_text(encoding="utf-8")).get(
            "recommendations", []
        )
        for extension in recommendations:
            if not extension:
                continue
            if self.dry_run:
                LOGGER.info("[Dry Run] Would install extension %s", extension)
                continue
            try:
                subprocess.run(
                    [str(code_cli), "--install-extension", extension, "--force"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                LOGGER.info("Ensured extension %s is installed", extension)
            except subprocess.CalledProcessError as exc:
                LOGGER.warning("Failed to install extension %s: %s", extension, exc)

    # endregion

    def install(self, category_ids: Sequence[str]) -> Dict[str, object]:
        categories = {c.identifier: c for c in self.available_categories()}
        if not category_ids:
            raise InstallationError("At least one task category must be selected.")
        missing = [identifier for identifier in category_ids if identifier not in categories]
        if missing:
            raise InstallationError(f"Unknown categories: {', '.join(missing)}")
        selected = [categories[identifier] for identifier in category_ids]

        LOGGER.info("Installing categories: %s", ", ".join(c.identifier for c in selected))
        code_cli = self._resolve_code_cli()
        vscode_dir = self._ensure_vscode_dir()
        tasks_path = vscode_dir / "tasks.json"
        backup = self._backup_file(tasks_path)

        existing = None
        if tasks_path.exists():
            try:
                existing = json.loads(tasks_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                LOGGER.warning("Existing tasks.json could not be parsed and will be replaced.")

        additions = [self._load_json(self._download_content(category)) for category in selected]
        merged = self._merge_tasks(existing, additions)
        self._write_json(tasks_path, merged)

        if self.settings_dir.exists():
            for name in ("settings.json", "keybindings.json", "extensions.json"):
                self._synchronize_file(self.settings_dir / name, vscode_dir / name)

        self._install_extensions(code_cli, self.settings_dir / "extensions.json")

        if not self.dry_run:
            try:
                json.loads(tasks_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise InstallationError(f"tasks.json validation failed: {exc}") from exc

        summary = {
            "categories": [category.identifier for category in selected],
            "tasks_path": str(tasks_path),
            "backup": str(backup) if backup else None,
            "tasks_count": len(merged.get("tasks", []) or []),
        }
        LOGGER.info("Installation summary: %s", summary)
        return summary

    def preview(self, category_ids: Sequence[str]) -> Dict[str, object]:
        categories = {c.identifier: c for c in self.available_categories()}
        additions = [self._load_json(self._download_content(categories[item])) for item in category_ids]
        merged = self._merge_tasks(None, additions)
        return {
            "categories": category_ids,
            "task_count": len(merged.get("tasks", []) or []),
            "input_count": len(merged.get("inputs", []) or []),
            "matcher_count": len(merged.get("problemMatchers", []) or []),
        }


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-platform installer for the VS Code productivity toolkit.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Examples:
            python setup.py --silent --categories python-general javascript-general
            python setup.py --remote-base-url https://raw.githubusercontent.com/DiogoRibeiro7/vscode-productivity-toolkit/main
            """
        ),
    )
    parser.add_argument("--categories", nargs="*", help="Task categories to install.")
    parser.add_argument("--source-root", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("--remote-base-url", help="Base URL for downloading task definitions.")
    parser.add_argument("--silent", action="store_true", help="Run without launching the GUI installer.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without modifying files.")
    parser.add_argument("--skip-extensions", action="store_true", help="Skip installing recommended extensions.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging output.")
    return parser.parse_args(argv)


class InstallerApp:
    def __init__(self, installer: TaskInstaller) -> None:
        if not tk or not ttk or not messagebox:
            raise InstallationError("Tkinter is not available on this system.")
        self.installer = installer
        self.root = tk.Tk()
        self.root.title("VS Code Productivity Toolkit Installer")
        self.root.geometry("640x480")
        self.categories = installer.available_categories()
        self.variables: Dict[str, tk.BooleanVar] = {
            category.identifier: tk.BooleanVar(value=True) for category in self.categories
        }
        self.status_text = tk.StringVar(value="Select categories and click Install.")
        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        heading = ttk.Label(frame, text="Select Task Categories", font=("Segoe UI", 14, "bold"))
        heading.pack(anchor=tk.W)

        description = ttk.Label(
            frame,
            text=(
                "Choose the automation suites to include in your VS Code tasks.json."
                " You can preview the resulting configuration before installing."
            ),
            wraplength=580,
            justify=tk.LEFT,
        )
        description.pack(anchor=tk.W, pady=(4, 12))

        tree = ttk.Treeview(frame, columns=("Description",), show="headings", height=8)
        tree.heading("Description", text="Description")
        tree.column("Description", width=420, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)

        for category in self.categories:
            tree.insert("", tk.END, iid=category.identifier, values=(category.description,))

        checklist = ttk.Frame(frame)
        checklist.pack(fill=tk.X, pady=12)

        for category in self.categories:
            cb = ttk.Checkbutton(
                checklist,
                text=category.label,
                variable=self.variables[category.identifier],
            )
            cb.pack(anchor=tk.W)

        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=(12, 0))

        preview_btn = ttk.Button(controls, text="Preview", command=self._preview)
        preview_btn.pack(side=tk.LEFT)

        install_btn = ttk.Button(controls, text="Install", command=self._install)
        install_btn.pack(side=tk.LEFT, padx=(8, 0))

        self.status = ttk.Label(frame, textvariable=self.status_text, foreground="#2563eb")
        self.status.pack(anchor=tk.W, pady=(16, 0))

    def _selected_categories(self) -> List[str]:
        selected = [identifier for identifier, var in self.variables.items() if var.get()]
        if not selected:
            raise InstallationError("Select at least one category before continuing.")
        return selected

    def _preview(self) -> None:
        try:
            categories = self._selected_categories()
            summary = self.installer.preview(categories)
            messagebox.showinfo(
                title="Preview",
                message=(
                    "Selected categories: {cats}\n"
                    "Tasks: {tasks}\nInputs: {inputs}\nProblem matchers: {matchers}"
                ).format(
                    cats=", ".join(summary["categories"]),
                    tasks=summary["task_count"],
                    inputs=summary["input_count"],
                    matchers=summary["matcher_count"],
                ),
            )
        except InstallationError as exc:
            messagebox.showerror("Preview failed", str(exc))

    def _install(self) -> None:
        try:
            categories = self._selected_categories()
        except InstallationError as exc:
            messagebox.showerror("Selection required", str(exc))
            return

        def worker() -> None:
            try:
                summary = self.installer.install(categories)
            except InstallationError as exc:
                messagebox.showerror("Installation failed", str(exc))
                self.status_text.set(f"Installation failed: {exc}")
                return
            self.status_text.set(f"Installation succeeded. tasks.json located at {summary['tasks_path']}")
            messagebox.showinfo(
                "Installation complete",
                f"Toolkit tasks installed with {summary['tasks_count']} tasks.",
            )

        threading.Thread(target=worker, daemon=True).start()

    def run(self) -> None:
        self.root.mainloop()


def run_cli(installer: TaskInstaller, categories: Sequence[str]) -> Dict[str, object]:
    try:
        return installer.install(categories)
    except InstallationError:
        installer.rollback.execute()
        raise


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_arguments(argv)
    configure_logging(args.verbose)
    project_root = Path(args.source_root).resolve()
    installer = TaskInstaller(
        project_root=project_root,
        dry_run=args.dry_run,
        remote_base_url=args.remote_base_url,
        skip_extensions=args.skip_extensions,
    )

    try:
        categories = args.categories or [category.identifier for category in installer.available_categories()]
        if args.silent or not tk:
            summary = run_cli(installer, categories)
            LOGGER.info("Toolkit installation complete: %s", summary)
            return 0
        app = InstallerApp(installer)
        for identifier in categories:
            if identifier in app.variables:
                app.variables[identifier].set(True)
        app.run()
        return 0
    except InstallationError as exc:
        LOGGER.error("Installation failed: %s", exc)
        installer.rollback.execute()
        return 1


if __name__ == "__main__":
    sys.exit(main())
