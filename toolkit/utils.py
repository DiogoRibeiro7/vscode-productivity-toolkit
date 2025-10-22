"""
MIT License
Copyright (c) 2025 Diogo Ribeiro

Utility functions and classes for the VS Code Productivity Toolkit.
"""

from __future__ import annotations

import logging
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class ProjectType(Enum):
    """Supported project types for detection."""
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    TYPESCRIPT = "TypeScript"
    REACT = "React"
    NODEJS = "Node.js"
    DOCKER = "Docker"
    GIT = "Git"
    DATA_SCIENCE = "Data Science"


class TaskCategory:
    """Task category management and validation."""
    
    # Available task categories
    AVAILABLE_CATEGORIES = {
        "python-general": {
            "name": "Python - General",
            "description": "Core Python development tasks: linting, testing, packaging",
            "project_types": [ProjectType.PYTHON],
            "task_count": 12,
        },
        "python-data-science": {
            "name": "Python - Data Science",
            "description": "Jupyter notebooks, profiling, documentation for data science",
            "project_types": [ProjectType.PYTHON, ProjectType.DATA_SCIENCE],
            "task_count": 8,
        },
        "javascript-general": {
            "name": "JavaScript - General",
            "description": "ESLint, Prettier, testing, and dependency management",
            "project_types": [ProjectType.JAVASCRIPT, ProjectType.TYPESCRIPT],
            "task_count": 10,
        },
        "javascript-node": {
            "name": "Node.js Services",
            "description": "Express development, databases, API testing, deployment",
            "project_types": [ProjectType.NODEJS],
            "task_count": 9,
        },
        "javascript-react": {
            "name": "React Applications",
            "description": "Component scaffolding, Storybook, bundle analysis, PWA",
            "project_types": [ProjectType.REACT],
            "task_count": 11,
        },
        "docker": {
            "name": "Docker Tasks",
            "description": "Container management, security scanning, orchestration",
            "project_types": [ProjectType.DOCKER],
            "task_count": 14,
        },
        "git": {
            "name": "Git Workflows",
            "description": "Branch management, hooks, conventional commits, automation",
            "project_types": [ProjectType.GIT],
            "task_count": 16,
        },
    }

    @classmethod
    def get_all_categories(cls) -> List[str]:
        """Get list of all available task category names."""
        return list(cls.AVAILABLE_CATEGORIES.keys())

    @classmethod
    def is_valid(cls, category: str) -> bool:
        """Check if a task category name is valid."""
        return category in cls.AVAILABLE_CATEGORIES

    @classmethod
    def get_info(cls, category: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific task category."""
        return cls.AVAILABLE_CATEGORIES.get(category)

    @classmethod
    def get_categories_for_project_type(cls, project_type: ProjectType) -> List[str]:
        """Get task categories suitable for a specific project type."""
        matching_categories = []
        for category, info in cls.AVAILABLE_CATEGORIES.items():
            if project_type in info["project_types"]:
                matching_categories.append(category)
        return matching_categories

    @classmethod
    def get_display_name(cls, category: str) -> str:
        """Get the display name for a task category."""
        info = cls.get_info(category)
        return info["name"] if info else category

    @classmethod
    def get_description(cls, category: str) -> str:
        """Get the description for a task category."""
        info = cls.get_info(category)
        return info["description"] if info else "No description available"


def setup_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    include_timestamp: bool = True
) -> None:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Logging level (e.g., logging.INFO, logging.DEBUG)
        format_string: Custom format string for log messages
        include_timestamp: Whether to include timestamp in log messages
    """
    if format_string is None:
        if include_timestamp:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        else:
            format_string = "%(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=level,
        format=format_string,
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
        force=True,  # Override any existing configuration
    )

    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


def validate_workspace(workspace_path: Union[str, Path]) -> Path:
    """
    Validate that a workspace path exists and is a directory.
    
    Args:
        workspace_path: Path to validate
        
    Returns:
        Resolved Path object
        
    Raises:
        ValidationError: If path is invalid
    """
    workspace = Path(workspace_path).resolve()
    
    if not workspace.exists():
        raise ValidationError(f"Workspace path does not exist: {workspace}")
    
    if not workspace.is_dir():
        raise ValidationError(f"Workspace path is not a directory: {workspace}")

    return workspace


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.1f} MB"
    else:
        return f"{size_bytes / (1024 ** 3):.1f} GB"


def truncate_string(text: str, max_length: int = 80, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        text: String to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add when truncating
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def parse_version(version_string: str) -> tuple[int, int, int]:
    """
    Parse a semantic version string into a tuple of integers.
    
    Args:
        version_string: Version string (e.g., "1.2.3")
        
    Returns:
        Tuple of (major, minor, patch) integers
        
    Raises:
        ValidationError: If version string is invalid
    """
    try:
        parts = version_string.strip().lstrip("v").split(".")
        if len(parts) != 3:
            raise ValueError("Version must have exactly 3 parts")
        
        return tuple(int(part) for part in parts)
    except (ValueError, AttributeError) as e:
        raise ValidationError(f"Invalid version string '{version_string}': {e}")


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two semantic version strings.
    
    Args:
        version1: First version string
        version2: Second version string
        
    Returns:
        -1 if version1 < version2, 0 if equal, 1 if version1 > version2
    """
    v1_parts = parse_version(version1)
    v2_parts = parse_version(version2)
    
    if v1_parts < v2_parts:
        return -1
    elif v1_parts > v2_parts:
        return 1
    else:
        return 0


# Convenience constants
DEFAULT_REPOSITORY_URL = "https://raw.githubusercontent.com/DiogoRibeiro7/vscode-productivity-toolkit/main"
SUPPORTED_VSCODE_VERSION = "^1.70.0"
TOOLKIT_VERSION = "1.0.0"

# Export commonly used items
__all__ = [
    "ValidationError",
    "ProjectType",
    "TaskCategory",
    "setup_logging",
    "validate_workspace",
    "format_file_size",
    "truncate_string",
    "parse_version",
    "compare_versions",
    "DEFAULT_REPOSITORY_URL",
    "SUPPORTED_VSCODE_VERSION",
    "TOOLKIT_VERSION",
]
