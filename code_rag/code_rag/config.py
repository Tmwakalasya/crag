"""Configuration helpers for code-rag."""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_DB_DIRNAME = ".code_rag_db"
DEFAULT_COLLECTION_NAME = "code_chunks"
DEFAULT_TOP_K = 5
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_OLLAMA_MODEL = "qwen2.5-coder"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"
ENV_DB_PATH = "CODE_RAG_DB_PATH"
ENV_COLLECTION_NAME = "CODE_RAG_COLLECTION"
ENV_TOP_K = "CODE_RAG_TOP_K"
ENV_GEMINI_MODEL = "CODE_RAG_GEMINI_MODEL"
ENV_OLLAMA_MODEL = "CODE_RAG_OLLAMA_MODEL"
ENV_OLLAMA_HOST = "OLLAMA_HOST"
ENV_GOOGLE_API_KEY = "GOOGLE_API_KEY"


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


def default_top_k() -> int:
    """Return the configured retrieval depth."""
    configured_value = os.getenv(ENV_TOP_K)
    return int(configured_value) if configured_value else DEFAULT_TOP_K


def gemini_model() -> str:
    """Return the configured Gemini model name."""
    return os.getenv(ENV_GEMINI_MODEL, DEFAULT_GEMINI_MODEL)


def ollama_model() -> str:
    """Return the configured Ollama model name."""
    return os.getenv(ENV_OLLAMA_MODEL, DEFAULT_OLLAMA_MODEL)


def ollama_host() -> str:
    """Return the configured Ollama host URL."""
    return os.getenv(ENV_OLLAMA_HOST, DEFAULT_OLLAMA_HOST)


def google_api_key() -> str | None:
    """Return the configured Google API key if present."""
    return os.getenv(ENV_GOOGLE_API_KEY)
