"""Vector search helpers for retrieving relevant code chunks."""

from __future__ import annotations

from pathlib import Path

from ..config import default_top_k
from ..indexer.db import get_collection, normalize_repo_root
from ..models import CodeChunk


def search_code_chunks(
    query: str,
    top_k: int | None = None,
    repo_root: str | Path | None = None,
) -> list[CodeChunk]:
    """Search the local vector store for code chunks relevant to a query."""
    collection = get_collection()
    limit = top_k or default_top_k()
    query_kwargs = {"query_texts": [query], "n_results": limit}
    if repo_root is not None:
        query_kwargs["where"] = {"repo_root": normalize_repo_root(repo_root)}
    results = collection.query(**query_kwargs)

    metadatas = results.get("metadatas", [[]])
    documents = results.get("documents", [[]])
    if not metadatas or not documents:
        return []

    return [
        _metadata_to_chunk(metadata, document)
        for metadata, document in zip(metadatas[0], documents[0], strict=False)
        if metadata is not None and document is not None
    ]


def _metadata_to_chunk(metadata: dict, document: str) -> CodeChunk:
    return CodeChunk(
        file_path=str(metadata["file_path"]),
        language=str(metadata["language"]),
        chunk_type=str(metadata["chunk_type"]),
        name=str(metadata["name"]),
        start_line=int(metadata["start_line"]),
        end_line=int(metadata["end_line"]),
        source_code=document,
        docstring=str(metadata["docstring"]) if "docstring" in metadata else None,
    )
