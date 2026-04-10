"""Parser engine that routes files to language-specific implementations."""

from __future__ import annotations

from pathlib import Path

from ..models import CodeChunk

from .go_parser import parse_go_source
from .py_parser import parse_python_source

SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".go": "go",
}


def detect_language(file_path: str | Path) -> str:
    """Infer the programming language from a file path."""
    suffix = Path(file_path).suffix.lower()
    try:
        return SUPPORTED_EXTENSIONS[suffix]
    except KeyError as error:
        raise ValueError(f"Unsupported file extension: {suffix or '<none>'}") from error


def parse_source(file_path: str | Path, source_code: str) -> list[CodeChunk]:
    """Parse raw source code into logical chunks."""
    language = detect_language(file_path)
    if language == "python":
        return parse_python_source(str(file_path), source_code)
    if language == "go":
        return parse_go_source(str(file_path), source_code)
    raise ValueError(f"No parser implementation is registered for language: {language}")


def parse_file(file_path: str | Path) -> list[CodeChunk]:
    """Read a source file from disk and parse it into chunks."""
    path = Path(file_path)
    return parse_source(path, path.read_text(encoding="utf-8"))
