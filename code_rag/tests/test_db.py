"""Tests for database helper logic that does not require ChromaDB."""

from __future__ import annotations

import importlib.util
import math
import unittest

DEPS_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if DEPS_AVAILABLE:
    from code_rag.code_rag.indexer.db import LocalHashEmbeddingFunction, chunk_id, chunk_to_metadata
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

        metadata = chunk_to_metadata(chunk)

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


if __name__ == "__main__":
    unittest.main()
