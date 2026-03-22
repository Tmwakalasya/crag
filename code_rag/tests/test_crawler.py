"""Tests for repository crawling helpers."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

DEPS_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if DEPS_AVAILABLE:
    from code_rag.code_rag.indexer.crawler import iter_source_files


@unittest.skipUnless(DEPS_AVAILABLE, "pydantic is not installed")
class CrawlerTest(unittest.TestCase):
    def test_iter_source_files_ignores_special_directories_and_binary_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "pkg").mkdir()
            (root / "pkg" / "keep.py").write_text("def keep():\n    return True\n", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git" / "ignored.py").write_text("ignored = True\n", encoding="utf-8")
            (root / "venv").mkdir()
            (root / "venv" / "ignored.py").write_text("ignored = True\n", encoding="utf-8")
            (root / "pkg" / "data.py").write_bytes(b"\x00\x01\x02")
            (root / "pkg" / "notes.txt").write_text("not python\n", encoding="utf-8")

            files = iter_source_files(root)

        self.assertEqual(files, [root / "pkg" / "keep.py"])


if __name__ == "__main__":
    unittest.main()
