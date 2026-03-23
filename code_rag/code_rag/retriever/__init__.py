"""Retrieval and answer-generation entry points for code-rag."""

from .generator import answer_query, generate_answer
from .search import search_code_chunks

__all__ = ["answer_query", "generate_answer", "search_code_chunks"]
