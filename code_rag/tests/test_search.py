"""Tests for retrieval search helpers."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

DEPS_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if DEPS_AVAILABLE:
    from code_rag.retriever.search import search_code_chunks


@unittest.skipUnless(DEPS_AVAILABLE, "pydantic is not installed")
class SearchTest(unittest.TestCase):
    def test_search_code_chunks_reconstructs_models_from_collection_results(self) -> None:
        fake_results = {
            "metadatas": [[
                {
                    "repo_root": "/tmp/repo",
                    "file_path": "src/demo.py",
                    "language": "python",
                    "chunk_type": "function",
                    "name": "demo",
                    "start_line": 4,
                    "end_line": 8,
                    "docstring": "Demo docstring.",
                }
            ]],
            "documents": [["def demo():\n    return True\n"]],
        }

        class FakeCollection:
            def count(self):
                return 10

            def query(self, **kwargs):
                self.kwargs = kwargs
                return fake_results

        collection = FakeCollection()
        with patch("code_rag.retriever.search.get_collection", return_value=collection):
            chunks = search_code_chunks("where is demo?", top_k=3, repo_root="/tmp/repo")

        self.assertEqual(collection.kwargs["query_texts"], ["where is demo?"])
        self.assertEqual(collection.kwargs["n_results"], 3)
        expected_root = str(Path("/tmp/repo").resolve())
        self.assertEqual(collection.kwargs["where"], {"repo_root": expected_root})
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].name, "demo")
        self.assertEqual(chunks[0].docstring, "Demo docstring.")


if __name__ == "__main__":
    unittest.main()
