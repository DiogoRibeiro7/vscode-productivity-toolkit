"""
# File Location: /toolkit/
MIT License
Copyright (c) 2025 Diogo Ribeiro

Task installation and management functionality.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import tempfile
import urllib.request
from urllib.parse import urlparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from .utils import TaskCategory, ValidationError

logger = logging.getLogger(__name__)


class TaskInstaller:
    """Handles installation and management of VS Code productivity tasks."""

    def __init__(self, workspace_path: Union[str, Path]):
        """
        Initialize the task installer.
        
        Args:
            workspace_path: Path to the VS Code workspace
        """
        self.workspace = Path(workspace_path).resolve()
        self.vscode_dir = self.workspace / ".vscode"
        self.tasks_file = self.vscode_dir / "tasks.json"
        self.backup_dir = self.vscode_dir / "backups"
        
        # Repository URL for downloading task definitions
        self.repository_url = "https://raw.githubusercontent.com/DiogoRibeiro7/vscode-productivity-toolkit/main"
        
        # Ensure .vscode directory exists
        self.vscode_dir.mkdir(exist_ok=True)

    def install_task_categories(
        self,
        categories: List[str],
        force: bool = False,
        create_backup: bool = True
    ) -> None:
        """
        Install the specified task categories.
        
        Args:
            categories: List of task category names to install
            force: Whether to overwrite existing tasks.json
            create_backup: Whether to create a backup before installation
        """
        logger.info(f"Installing task categories: {', '.join(categories)}")

        # Validate categories
        for category in categories:
            if not TaskCategory.is_valid(category):
                raise ValidationError(f"Invalid task category: {category}")

        # Preserve the original before merging or explicitly replacing it.
        if self.tasks_file.exists():
            if create_backup and self._create_backup() is None:
                raise ValidationError("Could not back up existing tasks.json")
            logger.info(
                "Replacing existing tasks.json" if force
                else "Merging with existing tasks.json"
            )

        # Download and merge task definitions
        task_definitions = []
        for category in categories:
            try:
                tasks = self._download_task_category(category)
                task_definitions.append((category, tasks))
                logger.info(f"Downloaded {category}: {len(tasks.get('tasks', []))} tasks")
            except Exception as e:
                logger.error(f"Failed to download {category}: {e}")
                raise

        # Merge and write tasks
        merged_tasks = self._merge_task_definitions(task_definitions, replace_existing=force)
        self._write_tasks_file(merged_tasks)

        logger.info(f"✅ Successfully installed {len(categories)} task categories")

    def _download_task_category(self, category: str) -> Dict[str, Any]:
        """Download task definition for a specific category."""
        url = self._get_category_url(category)
        
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != "raw.githubusercontent.com":
            raise ValidationError("Task repository URL must use HTTPS on raw.githubusercontent.com")

        try:
            with urllib.request.urlopen(url, timeout=30) as response:  # nosec B310 - URL validated above
                if response.status != 200:
                    raise ValidationError(f"HTTP {response.status}: Failed to download {category}")
                
                content = response.read().decode('utf-8')
                return json.loads(content)
                
        except urllib.error.URLError as e:
            raise ValidationError(f"Network error downloading {category}: {e}")
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON in {category}: {e}")

    def _get_category_url(self, category: str) -> str:
        """Get the download URL for a task category."""
        category_paths = {
            "python-general": "tasks/python/general.json",
            "python-data-science": "tasks/python/data-science.json",
            "javascript-general": "tasks/javascript/general.json",
            "javascript-node": "tasks/javascript/node.json",
            "javascript-react": "tasks/javascript/react.json",
            "docker": "tasks/docker/general.json",
            "git": "tasks/git/workflows.json",
        }
        
        path = category_paths.get(category)
        if not path:
            raise ValidationError(f"Unknown task category: {category}")
        
        return f"{self.repository_url}/{path}"

    @staticmethod
    def _prepare_metadata(
        raw_metadata: Any,
    ) -> Tuple[Union[Dict[str, Any], List[Any]], Dict[str, Any]]:
        """Preserve metadata from each installer and locate the CLI's tracking entry."""
        tracker: Dict[str, Any] = {
            "installedCategories": [],
            "lastUpdated": None,
            "version": "1.0.0",
        }

        if isinstance(raw_metadata, list):
            for entry in raw_metadata:
                if isinstance(entry, dict) and isinstance(
                    entry.get("installedCategories"), list
                ):
                    return raw_metadata, entry
            raw_metadata.append(tracker)
            return raw_metadata, tracker

        if isinstance(raw_metadata, dict):
            if not isinstance(raw_metadata.get("installedCategories"), list):
                raw_metadata["installedCategories"] = []
            return raw_metadata, raw_metadata

        return tracker, tracker

    def _merge_task_definitions(
        self, 
        task_definitions: List[tuple[str, Dict[str, Any]]],
        replace_existing: bool = False,
    ) -> Dict[str, Any]:
        """Merge task definitions, optionally replacing the existing task set."""
        
        # Load existing tasks if they exist
        existing_tasks = {}
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    existing_tasks = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                raise ValidationError(
                    f"Cannot read existing tasks.json at {self.tasks_file}: {e}"
                ) from e
            if not isinstance(existing_tasks, dict):
                raise ValidationError(
                    f"Existing tasks.json at {self.tasks_file} must be a JSON object"
                )

        if replace_existing:
            existing_tasks = {}

        # Shell installers store source metadata as a list; preserve that format.
        metadata, tracker = self._prepare_metadata(
            existing_tasks.get("_toolkitMetadata")
        )
        merged = {
            "version": "2.0.0",
            "tasks": existing_tasks.get("tasks", []),
            "inputs": existing_tasks.get("inputs", []),
            "problemMatchers": existing_tasks.get("problemMatchers", []),
            "_toolkitMetadata": metadata,
        }

        # Track existing task labels to avoid duplicates
        existing_labels = {task.get("label") for task in merged["tasks"]}
        existing_input_ids = {inp.get("id") for inp in merged["inputs"]}
        existing_matcher_names = {
            pm.get("name") if isinstance(pm, dict) else pm 
            for pm in merged["problemMatchers"]
        }

        # Merge each category
        for category, task_def in task_definitions:
            logger.debug(f"Merging category: {category}")

            # Merge tasks (avoid duplicates by label)
            for task in task_def.get("tasks", []):
                label = task.get("label")
                if label and label not in existing_labels:
                    merged["tasks"].append(task)
                    existing_labels.add(label)
                elif label:
                    logger.debug(f"Skipping duplicate task: {label}")

            # Merge inputs (avoid duplicates by id)
            for inp in task_def.get("inputs", []):
                inp_id = inp.get("id")
                if inp_id and inp_id not in existing_input_ids:
                    merged["inputs"].append(inp)
                    existing_input_ids.add(inp_id)

            # Merge problem matchers (avoid duplicates by name)
            for pm in task_def.get("problemMatchers", []):
                pm_name = pm.get("name") if isinstance(pm, dict) else pm
                if pm_name and pm_name not in existing_matcher_names:
                    merged["problemMatchers"].append(pm)
                    existing_matcher_names.add(pm_name)

            # Update metadata
            if category not in tracker["installedCategories"]:
                tracker["installedCategories"].append(category)

        # Update metadata
        tracker["lastUpdated"] = datetime.now().isoformat()
        
        return merged

    def _write_tasks_file(self, tasks: Dict[str, Any]) -> None:
        """Replace tasks.json only after the complete configuration is written."""
        destination = self.tasks_file.resolve()
        temporary_path: Optional[Path] = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=destination.parent,
                prefix=".tasks-",
                suffix=".json",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump(tasks, temporary_file, indent=2, ensure_ascii=False)

            if destination.exists():
                shutil.copymode(destination, temporary_path)
            os.replace(temporary_path, destination)
            logger.debug(f"Written tasks.json with {len(tasks.get('tasks', []))} tasks")
        except (OSError, TypeError, ValueError) as e:
            raise ValidationError(f"Failed to write tasks.json: {e}") from e
        finally:
            if temporary_path is not None:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError as e:
                    logger.warning(f"Could not remove temporary tasks file: {e}")

    def _create_backup(self) -> Path:
        """Create a backup of the current tasks.json file."""
        if not self.tasks_file.exists():
            logger.debug("No tasks.json to backup")
            return None

        # Ensure backup directory exists
        self.backup_dir.mkdir(exist_ok=True)

        # Create timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"tasks_backup_{timestamp}.json"

        try:
            shutil.copy2(self.tasks_file, backup_file)
            logger.info(f"Created backup: {backup_file.name}")
            return backup_file
        except OSError as e:
            logger.warning(f"Failed to create backup: {e}")
            return None

    def get_installed_tasks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all currently installed tasks organized by category."""
        if not self.tasks_file.exists():
            return {}

        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to read tasks.json: {e}")
            return {}

        # Group tasks by inferred category
        categorized_tasks = {}
        for task in tasks_data.get("tasks", []):
            category = self._infer_task_category(task.get("label", ""))
            if category not in categorized_tasks:
                categorized_tasks[category] = []
            categorized_tasks[category].append(task)

        return categorized_tasks

    def _infer_task_category(self, task_label: str) -> str:
        """Infer task category from task label."""
        if not task_label:
            return "unknown"
        
        label_lower = task_label.lower()
        
        if label_lower.startswith("python:"):
            return "python"
        elif label_lower.startswith(("js:", "javascript:", "node:", "npm:")):
            return "javascript"
        elif label_lower.startswith("react:"):
            return "react"
        elif label_lower.startswith("docker:"):
            return "docker"
        elif label_lower.startswith("git:"):
            return "git"
        else:
            return "general"
