"""Tests for answer generation helpers."""

from __future__ import annotations

import importlib.util
import os
import unittest
from unittest.mock import patch

DEPS_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if DEPS_AVAILABLE:
    from code_rag.code_rag.models import CodeChunk
    from code_rag.code_rag.retriever.generator import build_prompt, generate_answer


@unittest.skipUnless(DEPS_AVAILABLE, "pydantic is not installed")
class GeneratorTest(unittest.TestCase):
    def test_build_prompt_includes_query_and_chunk_metadata(self) -> None:
        chunk = CodeChunk(
            file_path="src/example.py",
            language="python",
            chunk_type="function",
            name="demo",
            start_line=2,
            end_line=4,
            source_code="def demo():\n    return True\n",
            docstring="Demo function.",
        )

        prompt = build_prompt("What does demo do?", [chunk])

        self.assertIn("What does demo do?", prompt)
        self.assertIn("src/example.py", prompt)
        self.assertIn("Demo function.", prompt)

    def test_generate_answer_uses_fallback_when_no_provider_is_available(self) -> None:
        chunk = CodeChunk(
            file_path="src/example.py",
            language="python",
            chunk_type="function",
            name="demo",
            start_line=2,
            end_line=4,
            source_code="def demo():\n    return True\n",
            docstring=None,
        )

        with patch.dict(os.environ, {}, clear=True):
            result = generate_answer("What does demo do?", [chunk])

        self.assertIn("No external LLM provider is configured", result.answer)
        self.assertEqual(result.referenced_chunks[0].name, "demo")


if __name__ == "__main__":
    unittest.main()
