"""
# File Location: /toolkit/
MIT License
Copyright (c) 2025 Diogo Ribeiro

Project type detection and task category suggestion logic.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple, Union

logger = logging.getLogger(__name__)


@dataclass
class ProjectDetectionResult:
    """Result of project type detection."""
    detected_types: List[str] = field(default_factory=list)
    confidence: Dict[str, float] = field(default_factory=dict)
    evidence: Dict[str, List[str]] = field(default_factory=dict)


class ProjectDetector:
    """Detects project types and suggests appropriate task categories."""

    def __init__(self):
        """Initialize the project detector with detection rules."""
        self.detection_rules = {
            "Python": {
                "files": [
                    "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg",
                    "Pipfile", "environment.yml", "conda.yml", "poetry.lock"
                ],
                "patterns": [r"\.py$", r"__pycache__"],
                "directories": ["__pycache__", ".venv", "venv"],
                "content_patterns": {
                    "pyproject.toml": [r'\[tool\.poetry\]', r'\[build-system\]'],
                    "requirements.txt": [r'^[a-zA-Z0-9\-_]+==.*$'],
                }
            },
            "JavaScript": {
                "files": ["package.json", "yarn.lock", "package-lock.json"],
                "patterns": [r"\.js$", r"\.mjs$", r"\.cjs$"],
                "directories": ["node_modules", ".npm"],
                "content_patterns": {
                    "package.json": [r'"dependencies":', r'"devDependencies":'],
                }
            },
            "TypeScript": {
                "files": ["tsconfig.json", "tslint.json", ".eslintrc.ts"],
                "patterns": [r"\.ts$", r"\.tsx$", r"\.d\.ts$"],
                "directories": ["dist", "build"],
                "content_patterns": {
                    "tsconfig.json": [r'"compilerOptions":', r'"typescript"'],
                    "package.json": [r'"typescript":', r'"@types/'],
                }
            },
            "React": {
                "files": ["public/index.html", ".babelrc", "craco.config.js"],
                "patterns": [r"\.jsx$", r"\.tsx$"],
                "directories": ["public", "src", "build"],
                "content_patterns": {
                    "package.json": [
                        r'"react":', r'"react-dom":', r'"react-scripts":',
                        r'"@types/react":', r'"create-react-app"'
                    ],
                }
            },
            "Node.js": {
                "files": ["server.js", "app.js", "index.js"],
                "patterns": [r"routes/.*\.js$", r"middleware/.*\.js$"],
                "directories": ["routes", "middleware", "controllers", "models"],
                "content_patterns": {
                    "package.json": [
                        r'"express":', r'"fastify":', r'"koa":', r'"nest"',
                        r'"node":', r'"nodemon":'
                    ],
                }
            },
            "Docker": {
                "files": [
                    "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
                    ".dockerignore", "Dockerfile.dev", "Dockerfile.prod"
                ],
                "patterns": [r"Dockerfile.*"],
                "directories": [".docker"],
                "content_patterns": {
                    "Dockerfile": [r'^FROM\s+', r'^RUN\s+', r'^COPY\s+'],
                    "docker-compose.yml": [r'version:', r'services:', r'volumes:'],
                }
            },
            "Git": {
                "files": [".gitignore", ".gitattributes"],
                "patterns": [],
                "directories": [".git"],
                "content_patterns": {}
            },
            "Data Science": {
                "files": ["environment.yml", "conda.yml"],
                "patterns": [r"\.ipynb$", r".*\.pkl$", r".*\.csv$"],
                "directories": ["data", "notebooks", "models"],
                "content_patterns": {
                    "requirements.txt": [
                        r'pandas', r'numpy', r'scipy', r'matplotlib',
                        r'seaborn', r'jupyter', r'scikit-learn'
                    ],
                    "environment.yml": [r'pandas', r'numpy', r'jupyter'],
                }
            }
        }

        self.task_category_mapping = {
            "Python": ["python-general"],
            "JavaScript": ["javascript-general"],
            "TypeScript": ["javascript-general"],
            "React": ["javascript-react", "javascript-general"],
            "Node.js": ["javascript-node", "javascript-general"],
            "Docker": ["docker"],
            "Git": ["git"],
            "Data Science": ["python-data-science", "python-general"],
        }

    def detect_project_type(self, workspace_path: Union[str, Path]) -> ProjectDetectionResult:
        """
        Detect project types in the given workspace.
        
        Args:
            workspace_path: Path to the workspace directory
            
        Returns:
            ProjectDetectionResult with detected types, confidence scores, and evidence
        """
        workspace = Path(workspace_path).resolve()
        
        if not workspace.is_dir():
            raise ValueError(f"Workspace path is not a directory: {workspace}")

        logger.info(f"Detecting project type in: {workspace}")

        result = ProjectDetectionResult()
        
        for project_type, rules in self.detection_rules.items():
            confidence, evidence = self._calculate_confidence(workspace, project_type, rules)
            
            if confidence > 0.3:  # Threshold for detection
                result.detected_types.append(project_type)
                result.confidence[project_type] = confidence
                result.evidence[project_type] = evidence

        # Sort by confidence
        result.detected_types.sort(key=lambda x: result.confidence[x], reverse=True)

        logger.info(f"Detected {len(result.detected_types)} project types")
        return result

    def _calculate_confidence(
        self, 
        workspace: Path, 
        project_type: str, 
        rules: Dict
    ) -> Tuple[float, List[str]]:
        """Calculate confidence score for a project type."""
        evidence = []
        score = 0.0
        max_score = 0.0

        # Check for specific files
        for file_name in rules.get("files", []):
            max_score += 0.15
            file_path = workspace / file_name
            if file_path.exists():
                score += 0.15
                evidence.append(f"File: {file_name}")

        # Check for file patterns
        for pattern in rules.get("patterns", []):
            max_score += 0.1
            if self._find_files_matching_pattern(workspace, pattern):
                score += 0.1
                evidence.append(f"Pattern: {pattern}")

        # Check for directories
        for dir_name in rules.get("directories", []):
            max_score += 0.1
            dir_path = workspace / dir_name
            if dir_path.is_dir():
                score += 0.1
                evidence.append(f"Directory: {dir_name}")

        # Check content patterns
        content_patterns = rules.get("content_patterns", {})
        for file_name, patterns in content_patterns.items():
            file_path = workspace / file_name
            if file_path.exists():
                for pattern in patterns:
                    max_score += 0.05
                    if self._file_contains_pattern(file_path, pattern):
                        score += 0.05
                        evidence.append(f"Content: {file_name} contains {pattern}")

        # Normalize confidence to 0-1 range
        confidence = score / max_score if max_score > 0 else 0.0
        
        # Apply bonus for multiple strong indicators
        if len(evidence) >= 3:
            confidence = min(1.0, confidence * 1.2)

        return confidence, evidence

    def _find_files_matching_pattern(self, workspace: Path, pattern: str) -> bool:
        """Check if any files match the given regex pattern."""
        try:
            compiled_pattern = re.compile(pattern)
            for file_path in workspace.rglob("*"):
                if file_path.is_file() and compiled_pattern.search(str(file_path.relative_to(workspace))):
                    return True
        except re.error:
            logger.warning(f"Invalid regex pattern: {pattern}")
        return False

    def _file_contains_pattern(self, file_path: Path, pattern: str) -> bool:
        """Check if file content matches the given regex pattern."""
        try:
            compiled_pattern = re.compile(pattern, re.MULTILINE)
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            return bool(compiled_pattern.search(content))
        except (OSError, re.error) as e:
            logger.debug(f"Could not check pattern in {file_path}: {e}")
            return False

    def suggest_task_categories(self, detection_result: ProjectDetectionResult) -> List[str]:
        """
        Suggest task categories based on detected project types.
        
        Args:
            detection_result: Result from detect_project_type()
            
        Returns:
            List of recommended task category names
        """
        suggested_categories = set()
        
        for project_type in detection_result.detected_types:
            categories = self.task_category_mapping.get(project_type, [])
            suggested_categories.update(categories)

        # Always suggest git if it's available
        if any(ptype in detection_result.detected_types for ptype in ["Git"]):
            suggested_categories.add("git")

        # Convert to sorted list for consistent ordering
        return sorted(list(suggested_categories))

    def get_detection_summary(self, detection_result: ProjectDetectionResult) -> str:
        """Get a human-readable summary of detection results."""
        if not detection_result.detected_types:
            return "No specific project type detected."

        summary_lines = [
            f"Detected {len(detection_result.detected_types)} project type(s):",
        ]

        for project_type in detection_result.detected_types:
            confidence = detection_result.confidence.get(project_type, 0)
            evidence_count = len(detection_result.evidence.get(project_type, []))
            summary_lines.append(
                f"  • {project_type}: {confidence:.1%} confidence "
                f"({evidence_count} indicators)"
            )

        suggested_categories = self.suggest_task_categories(detection_result)
        if suggested_categories:
            summary_lines.append(f"\nRecommended task categories: {', '.join(suggested_categories)}")

        return "\n".join(summary_lines)

    def validate_workspace(self, workspace_path: Union[str, Path]) -> Path:
        """Validate that the workspace path exists and is a directory."""
        workspace = Path(workspace_path).resolve()
        
        if not workspace.exists():
            raise ValueError(f"Workspace path does not exist: {workspace}")
        
        if not workspace.is_dir():
            raise ValueError(f"Workspace path is not a directory: {workspace}")

        return workspace

    def get_supported_project_types(self) -> List[str]:
        """Get list of all supported project types."""
        return list(self.detection_rules.keys())

    def get_available_task_categories(self) -> Set[str]:
        """Get set of all available task categories."""
        categories = set()
        for category_list in self.task_category_mapping.values():
            categories.update(category_list)
        return categories
