"""ChromaDB persistence helpers for code-rag."""

from __future__ import annotations

import hashlib
import importlib
import math
import re
from pathlib import Path

from ..config import collection_name, db_path
from ..models import CodeChunk

_EMBEDDING_DIMENSION = 256
_TOKEN_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


class LocalHashEmbeddingFunction:
    """A deterministic local embedding function that avoids network downloads."""

    def __call__(self, input: list[str]) -> list[list[float]]:
        return [self._embed_document(document) for document in input]

    def _embed_document(self, document: str) -> list[float]:
        vector = [0.0] * _EMBEDDING_DIMENSION
        for token in _TOKEN_PATTERN.findall(document.lower()):
            digest = hashlib.sha1(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % _EMBEDDING_DIMENSION
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector
        return [value / magnitude for value in vector]


def get_client():
    """Create a persistent local ChromaDB client."""
    chromadb = importlib.import_module("chromadb")
    storage_path = db_path()
    storage_path.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(storage_path))


def get_collection(client=None):
    """Return the code chunk collection, creating it if necessary."""
    client = client or get_client()
    return client.get_or_create_collection(
        name=collection_name(),
        embedding_function=LocalHashEmbeddingFunction(),
    )


def normalize_repo_root(repo_root: str | Path) -> str:
    """Normalize a repository root for storage and filtering."""
    return str(Path(repo_root).expanduser().resolve())


def chunk_id(chunk: CodeChunk) -> str:
    """Build a stable identifier for a code chunk."""
    raw_identifier = (
        f"{chunk.file_path}:{chunk.chunk_type}:{chunk.name}:{chunk.start_line}:{chunk.end_line}"
    )
    return hashlib.sha1(raw_identifier.encode("utf-8")).hexdigest()


def chunk_to_metadata(chunk: CodeChunk, repo_root: str | Path) -> dict[str, str | int]:
    """Convert a code chunk into ChromaDB metadata."""
    metadata: dict[str, str | int] = {
        "repo_root": normalize_repo_root(repo_root),
        "file_path": chunk.file_path,
        "language": chunk.language,
        "chunk_type": chunk.chunk_type,
        "name": chunk.name,
        "start_line": chunk.start_line,
        "end_line": chunk.end_line,
    }
    if chunk.docstring:
        metadata["docstring"] = chunk.docstring
    return metadata


def _build_document_text(chunk: CodeChunk) -> str:
    """Build enriched document text that includes metadata for better search.

    The hash-based embeddings match on token overlap, so including the file
    name, chunk name, type, and docstring in the indexed text dramatically
    improves retrieval quality.
    """
    file_name = Path(chunk.file_path).name
    header_parts = [
        f"file: {file_name}",
        f"{chunk.chunk_type}: {chunk.name}",
        f"language: {chunk.language}",
    ]
    if chunk.docstring:
        header_parts.append(f"docstring: {chunk.docstring}")
    header = "\n".join(header_parts)
    return f"{header}\n\n{chunk.source_code}"


def ingest_chunks(chunks: list[CodeChunk], repo_root: str | Path) -> int:
    """Replace the indexed chunks for a repository in the local ChromaDB collection."""
    collection = get_collection()
    repo_scope = normalize_repo_root(repo_root)
    collection.delete(where={"repo_root": repo_scope})

    if not chunks:
        return 0

    payload = {
        "ids": [chunk_id(chunk) for chunk in chunks],
        "documents": [_build_document_text(chunk) for chunk in chunks],
        "metadatas": [chunk_to_metadata(chunk, repo_root=repo_scope) for chunk in chunks],
    }

    collection.upsert(**payload)
    return len(chunks)
