"""Shared Pydantic models for parsing, retrieval, and generation."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class CodeChunk(BaseModel):
    """A logical unit of source code extracted from a repository."""

    file_path: str
    language: str
    chunk_type: Literal["function", "class", "method", "global_scope"]
    name: str
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    source_code: str
    docstring: str | None = None


class QueryResult(BaseModel):
    """Structured answer returned from a retrieval and generation workflow."""

    answer: str
    referenced_chunks: list[CodeChunk]
