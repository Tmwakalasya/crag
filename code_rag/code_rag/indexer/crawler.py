"""Directory crawling utilities for repository ingestion."""

from __future__ import annotations

import os
from pathlib import Path

from ..models import CodeChunk
from ..parser.engine import SUPPORTED_EXTENSIONS, parse_file

IGNORED_DIRECTORIES = {
    ".git",
    ".idea",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
}


def iter_source_files(root_dir: str | Path) -> list[Path]:
    """Return supported source files under the target directory."""
    root_path = Path(root_dir).expanduser().resolve()
    source_files: list[Path] = []

    for current_root, dir_names, file_names in os.walk(root_path):
        dir_names[:] = sorted(
            directory_name
            for directory_name in dir_names
            if directory_name not in IGNORED_DIRECTORIES
        )

        current_root_path = Path(current_root)
        for file_name in sorted(file_names):
            path = current_root_path / file_name
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if _is_binary_file(path):
                continue
            source_files.append(path)

    return source_files


def crawl_code_chunks(root_dir: str | Path) -> list[CodeChunk]:
    """Parse all supported source files beneath the target directory."""
    chunks: list[CodeChunk] = []
    for path in iter_source_files(root_dir):
        chunks.extend(parse_file(path))
    return chunks


def _is_binary_file(path: Path, sample_size: int = 1024) -> bool:
    sample = path.read_bytes()[:sample_size]
    if b"\x00" in sample:
        return True

    try:
        sample.decode("utf-8")
    except UnicodeDecodeError:
        return True

    return False
