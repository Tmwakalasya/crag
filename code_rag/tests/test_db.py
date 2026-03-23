"""Tests for database helper logic that does not require ChromaDB."""

from __future__ import annotations

import importlib.util
import math
import unittest
from unittest.mock import patch

DEPS_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if DEPS_AVAILABLE:
    from code_rag.code_rag.indexer.db import (
        LocalHashEmbeddingFunction,
        chunk_id,
        chunk_to_metadata,
        ingest_chunks,
        normalize_repo_root,
    )
    from code_rag.code_rag.models import CodeChunk


@unittest.skipUnless(DEPS_AVAILABLE, "pydantic is not installed")
class DatabaseHelperTest(unittest.TestCase):
    def test_chunk_to_metadata_and_chunk_id_are_stable(self) -> None:
        chunk = CodeChunk(
            file_path="src/example.py",
            language="python",
            chunk_type="function",
            name="demo",
            start_line=3,
            end_line=6,
            source_code="def demo():\n    return True\n",
            docstring="Demo function.",
        )

        metadata = chunk_to_metadata(chunk, repo_root="/tmp/repo")

        self.assertEqual(metadata["repo_root"], normalize_repo_root("/tmp/repo"))
        self.assertEqual(metadata["file_path"], "src/example.py")
        self.assertEqual(metadata["start_line"], 3)
        self.assertEqual(metadata["docstring"], "Demo function.")
        self.assertEqual(chunk_id(chunk), chunk_id(chunk))

    def test_local_hash_embedding_function_is_deterministic(self) -> None:
        embedder = LocalHashEmbeddingFunction()

        embeddings = embedder(["def demo(): return True", "def demo(): return True"])

        self.assertEqual(len(embeddings), 2)
        self.assertEqual(embeddings[0], embeddings[1])
        self.assertTrue(math.isclose(sum(value * value for value in embeddings[0]), 1.0))

    def test_ingest_replaces_existing_chunks_for_repo_scope(self) -> None:
        chunk = CodeChunk(
            file_path="src/example.py",
            language="python",
            chunk_type="function",
            name="demo",
            start_line=1,
            end_line=2,
            source_code="def demo():\n    return True\n",
        )

        class FakeCollection:
            def __init__(self) -> None:
                self.deleted_where = None
                self.upsert_payload = None

            def delete(self, where):
                self.deleted_where = where

            def upsert(self, **payload):
                self.upsert_payload = payload

        collection = FakeCollection()
        with patch("code_rag.code_rag.indexer.db.get_collection", return_value=collection):
            count = ingest_chunks([chunk], repo_root="/tmp/repo")

        self.assertEqual(count, 1)
        self.assertEqual(collection.deleted_where, {"repo_root": normalize_repo_root("/tmp/repo")})
        self.assertEqual(collection.upsert_payload["metadatas"][0]["repo_root"], normalize_repo_root("/tmp/repo"))


if __name__ == "__main__":
    unittest.main()
