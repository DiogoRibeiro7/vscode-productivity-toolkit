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

Documentation validation helpers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Sequence

CODE_BLOCK_PATTERN = re.compile(r"^```(?P<language>[\w+-]*)\s*$")
LINK_PATTERN = re.compile(r"\[(?P<label>[^\]]+)\]\((?P<link>[^)]+)\)")


@dataclass(frozen=True)
class CodeBlockFinding:
    """Represents the validation status for a code block."""

    path: Path
    line: int
    language: str
    is_valid: bool


@dataclass(frozen=True)
class LinkFinding:
    """Represents the validation status for a hyperlink reference."""

    path: Path
    link: str
    is_valid: bool


def iter_markdown_files(base_path: Path) -> Iterator[Path]:
    """Yield all Markdown files that require validation."""

    for directory in ("docs", "examples", "README.md", "tests/README.md"):
        target = base_path / directory if directory != "README.md" else base_path / "README.md"
        if target.is_file():
            yield target
        elif target.is_dir():
            yield from sorted(target.rglob("*.md"))


def validate_code_blocks(path: Path) -> List[CodeBlockFinding]:
    """Ensure each fenced code block declares a language identifier."""

    findings: List[CodeBlockFinding] = []
    in_block = False
    with path.open("r", encoding="utf-8") as handle:
        for index, raw_line in enumerate(handle, start=1):
            match = CODE_BLOCK_PATTERN.match(raw_line.rstrip("\n"))
            if match:
                language = match.group("language").strip()
                if not in_block:
                    findings.append(
                        CodeBlockFinding(
                            path=path,
                            line=index,
                            language=language,
                            is_valid=bool(language),
                        )
                    )
                    in_block = True
                else:
                    in_block = False
    return findings


def validate_links(path: Path, base_path: Path) -> List[LinkFinding]:
    """Validate that relative links resolve to existing files."""

    findings: List[LinkFinding] = []
    content = path.read_text(encoding="utf-8")
    for match in LINK_PATTERN.finditer(content):
        link = match.group("link")
        if link.startswith("http") or link.startswith("mailto:"):
            findings.append(LinkFinding(path=path, link=link, is_valid=True))
            continue
        if link.startswith("#"):
            findings.append(LinkFinding(path=path, link=link, is_valid=True))
            continue
        if "#" in link:
            target, anchor = link.split("#", 1)
        else:
            target, anchor = link, ""
        resolved = (path.parent / target).resolve()
        exists = resolved.exists()
        if exists and anchor:
            findings.append(LinkFinding(path=path, link=link, is_valid=True))
            continue
        findings.append(LinkFinding(path=path, link=link, is_valid=exists))
    return findings


def load_markdown_metadata(path: Path) -> Dict[str, Sequence[str]]:
    """Extract optional QA metadata blocks for executable examples."""

    metadata: Dict[str, Sequence[str]] = {}
    content = path.read_text(encoding="utf-8")
    markers = re.findall(r"<!--\s*qa:(?P<key>[\w-]+)\s*=\s*(?P<value>[^-]+)-->", content)
    for key, value in markers:
        commands = [command.strip() for command in value.split("&&") if command.strip()]
        metadata[key] = commands
    return metadata
