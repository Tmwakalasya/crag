"""Configuration helpers for code-rag."""

from __future__ import annotations

from pathlib import Path

DEFAULT_DB_DIRNAME = ".code_rag_db"
ENV_DB_PATH = "CODE_RAG_DB_PATH"


def default_db_path() -> Path:
    """Return the default persistent ChromaDB storage path."""
    return Path.home() / DEFAULT_DB_DIRNAME
