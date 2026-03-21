"""Configuration helpers for code-rag."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_DB_DIRNAME = ".code_rag_db"
DEFAULT_COLLECTION_NAME = "code_chunks"
ENV_DB_PATH = "CODE_RAG_DB_PATH"
ENV_COLLECTION_NAME = "CODE_RAG_COLLECTION"


def default_db_path() -> Path:
    """Return the default persistent ChromaDB storage path."""
    return Path.home() / DEFAULT_DB_DIRNAME


def db_path() -> Path:
    """Return the configured persistent ChromaDB storage path."""
    configured_path = os.getenv(ENV_DB_PATH)
    return Path(configured_path).expanduser() if configured_path else default_db_path()


def collection_name() -> str:
    """Return the configured ChromaDB collection name."""
    return os.getenv(ENV_COLLECTION_NAME, DEFAULT_COLLECTION_NAME)
