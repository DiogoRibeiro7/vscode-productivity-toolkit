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

Utility functions for configuring structured logging across the toolkit.
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    """A logging formatter that outputs JSON strings for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        base: Dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
        }
        if record.exc_info:
            base["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            base["stack"] = self.formatStack(record.stack_info)
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            base.update(record.extra)
        return json.dumps(base)


def configure_logging(level: str = "INFO", *, use_json: bool = True) -> None:
    """Configure logging for the toolkit."""

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level, handlers=[])

    handler = logging.StreamHandler(stream=sys.stdout)
    if use_json:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(numeric_level)


def get_logger(name: str) -> logging.Logger:
    """Retrieve a logger configured for the toolkit."""

    return logging.getLogger(name)
