"""Prompt construction and answer generation for retrieved code chunks."""

from __future__ import annotations

import importlib
import importlib.util
from textwrap import dedent

from ..config import (
    ENV_OLLAMA_HOST,
    ENV_OLLAMA_MODEL,
    gemini_model,
    google_api_key,
    ollama_host,
    ollama_model,
)
from ..models import CodeChunk, QueryResult
from .search import search_code_chunks

_SYSTEM_PROMPT = (
    "You are an expert software architect. Answer the user's question based strictly "
    "on the provided code chunks. If the answer is uncertain, say so plainly."
)


def answer_query(query: str, top_k: int | None = None) -> QueryResult:
    """Retrieve relevant chunks and generate a grounded answer."""
    chunks = search_code_chunks(query, top_k=top_k)
    return generate_answer(query, chunks)


def generate_answer(query: str, chunks: list[CodeChunk]) -> QueryResult:
    """Generate an answer for a query using retrieved chunks."""
    if not chunks:
        return QueryResult(
            answer="No indexed code chunks matched the query. Run `crag ingest` first or try a broader question.",
            referenced_chunks=[],
        )

    prompt = build_prompt(query, chunks)
    answer = _generate_with_gemini(prompt) or _generate_with_ollama(prompt) or _fallback_answer(
        query,
        chunks,
    )
    return QueryResult(answer=answer, referenced_chunks=chunks)


def build_prompt(query: str, chunks: list[CodeChunk]) -> str:
    """Construct the grounded prompt sent to the selected answer generator."""
    chunk_sections = [
        dedent(
            f"""
            File: {chunk.file_path}
            Language: {chunk.language}
            Chunk type: {chunk.chunk_type}
            Name: {chunk.name}
            Lines: {chunk.start_line}-{chunk.end_line}
            Docstring: {chunk.docstring or '<none>'}
            Source:
            {chunk.source_code}
            """
        ).strip()
        for chunk in chunks
    ]

    return (
        f"System: {_SYSTEM_PROMPT}\n\n"
        f"User question: {query}\n\n"
        "Relevant code chunks:\n\n"
        + "\n\n---\n\n".join(chunk_sections)
    )


def _generate_with_gemini(prompt: str) -> str | None:
    api_key = google_api_key()
    if not api_key or importlib.util.find_spec("google") is None:
        return None

    genai = importlib.import_module("google.genai")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=gemini_model(), contents=prompt)
    return getattr(response, "text", None)


def _generate_with_ollama(prompt: str) -> str | None:
    import os

    if (
        importlib.util.find_spec("ollama") is None
        or (ENV_OLLAMA_MODEL not in os.environ and ENV_OLLAMA_HOST not in os.environ)
    ):
        return None

    ollama = importlib.import_module("ollama")
    client = ollama.Client(host=ollama_host())
    try:
        response = client.generate(model=ollama_model(), prompt=prompt)
    except Exception:
        return None
    return response.get("response")


def _fallback_answer(query: str, chunks: list[CodeChunk]) -> str:
    references = "\n".join(
        f"- {chunk.file_path}:{chunk.start_line}-{chunk.end_line} ({chunk.chunk_type} {chunk.name})"
        for chunk in chunks
    )
    highlights = "\n\n".join(
        dedent(
            f"""
            {chunk.file_path}:{chunk.start_line}-{chunk.end_line}
            {chunk.source_code[:400].strip()}
            """
        ).strip()
        for chunk in chunks[:3]
    )
    return dedent(
        f"""
        No external LLM provider is configured, so this is a grounded fallback summary.

        Question: {query}

        Most relevant chunks:
        {references}

        Relevant excerpts:
        {highlights}
        """
    ).strip()
