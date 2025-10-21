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

Quality checks for the documentation set.
"""

from __future__ import annotations

from pathlib import Path

from qa.documentation import (
    iter_markdown_files,
    load_markdown_metadata,
    validate_code_blocks,
    validate_links,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_markdown_code_blocks_declare_language() -> None:
    findings = []
    for path in iter_markdown_files(PROJECT_ROOT):
        findings.extend(validate_code_blocks(path))
    missing = [finding for finding in findings if not finding.is_valid]
    if missing:
        sample = missing[:5]
        raise AssertionError(
            f"Code blocks missing language identifiers (sample): {sample}"
        )


def test_relative_links_resolve() -> None:
    findings = []
    for path in iter_markdown_files(PROJECT_ROOT):
        findings.extend(validate_links(path, PROJECT_ROOT))
    broken = [finding for finding in findings if not finding.is_valid]
    if broken:
        sample = broken[:5]
        raise AssertionError(f"Broken documentation links detected (sample): {sample}")


def test_documentation_metadata_is_well_formed() -> None:
    for path in iter_markdown_files(PROJECT_ROOT):
        metadata = load_markdown_metadata(path)
        for key, commands in metadata.items():
            assert commands, f"Metadata '{key}' in {path} must contain commands"
