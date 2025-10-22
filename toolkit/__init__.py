"""
# File Location: /toolkit/
MIT License
Copyright (c) 2025 Diogo Ribeiro

VS Code Productivity Toolkit - Python Package
==============================================

Enterprise-grade automation toolkit with curated tasks, smart project detection,
and seamless VS Code integration.

Author: Diogo Ribeiro <dfr@esmad.ipp.pt>
ORCID: https://orcid.org/0009-0001-2022-7072
"""

from __future__ import annotations

__version__ = "1.0.0"
__author__ = "Diogo Ribeiro"
__email__ = "dfr@esmad.ipp.pt"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 Diogo Ribeiro"

# Import main classes for easy access
from .detector import ProjectDetector
from .installer import TaskInstaller
from .cli import main as cli_main
from .utils import TaskCategory, ProjectType, ValidationError

__all__ = [
    "ProjectDetector",
    "TaskInstaller", 
    "cli_main",
    "TaskCategory",
    "ProjectType",
    "ValidationError",
    "__version__",
    "__author__",
    "__email__",
]

# Package metadata
PACKAGE_INFO = {
    "name": "vscode-productivity-toolkit",
    "version": __version__,
    "description": "Enterprise-grade VS Code automation toolkit",
    "author": __author__,
    "author_email": __email__,
    "license": __license__,
    "url": "https://github.com/DiogoRibeiro7/vscode-productivity-toolkit",
    "keywords": ["vscode", "productivity", "automation", "development"],
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Text Editors :: Integrated Development Environments (IDE)",
    ],
}
