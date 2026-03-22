"""CLI smoke tests for installable and module-level entry points."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

DEPS_AVAILABLE = (
    importlib.util.find_spec("pydantic") is not None
    and importlib.util.find_spec("typer") is not None
)

if DEPS_AVAILABLE:
    from typer.testing import CliRunner

    from code_rag.code_rag.main import app
    from code_rag.code_rag.models import CodeChunk, QueryResult


@unittest.skipUnless(DEPS_AVAILABLE, "pydantic and typer are not installed")
class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_ingest_command_prints_summary(self) -> None:
        chunk = CodeChunk(
            file_path="src/example.py",
            language="python",
            chunk_type="function",
            name="demo",
            start_line=1,
            end_line=2,
            source_code="def demo():\n    return True\n",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir)
            with patch("code_rag.code_rag.indexer.crawler.iter_source_files", return_value=[target_dir / "example.py"]), patch(
                "code_rag.code_rag.indexer.crawler.crawl_code_chunks",
                return_value=[chunk],
            ), patch("code_rag.code_rag.indexer.db.ingest_chunks", return_value=1):
                result = self.runner.invoke(app, ["ingest", str(target_dir)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Chunks indexed", result.stdout)
        self.assertIn("1", result.stdout)

    def test_ask_command_prints_answer_and_references(self) -> None:
        chunk = CodeChunk(
            file_path="src/example.py",
            language="python",
            chunk_type="function",
            name="demo",
            start_line=10,
            end_line=12,
            source_code="def demo():\n    return True\n",
        )
        query_result = QueryResult(answer="demo lives in src/example.py", referenced_chunks=[chunk])

        with patch(
            "code_rag.code_rag.retriever.generator.answer_query",
            return_value=query_result,
        ):
            result = self.runner.invoke(app, ["ask", "Where is demo?"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("demo lives in src/example.py", result.stdout)
        self.assertIn("src/example.py", result.stdout)
        self.assertIn("10-12", result.stdout)


if __name__ == "__main__":
    unittest.main()
