"""Standalone tests for the Python parser."""

from __future__ import annotations

import importlib.util
import unittest

PARSER_DEPS_AVAILABLE = all(
    importlib.util.find_spec(module_name) is not None
    for module_name in ("pydantic", "tree_sitter", "tree_sitter_python")
)

if PARSER_DEPS_AVAILABLE:
    from code_rag.parser.engine import parse_source


@unittest.skipUnless(PARSER_DEPS_AVAILABLE, "parser dependencies are not installed")
class PythonParserTest(unittest.TestCase):
    def test_python_source_splits_into_expected_chunks(self) -> None:
        source_code = '''"""Module docs."""

import os

VALUE = 7


def helper(name: str) -> str:
    """Return a friendly message."""
    return f"Hello, {name}!"


class Greeter:
    """Greets users."""

    def greet(self, target: str) -> str:
        """Build a greeting."""
        return helper(target)

    async def async_greet(self, target: str) -> str:
        """Build an async greeting."""
        return self.greet(target)


if __name__ == "__main__":
    print(helper("world"))
'''
        chunks = parse_source("sample.py", source_code)

        self.assertEqual(
            [chunk.chunk_type for chunk in chunks],
            ["global_scope", "function", "class", "method", "method", "global_scope"],
        )
        self.assertEqual(
            [chunk.name for chunk in chunks[:5]],
            ["global_scope_0", "helper", "Greeter", "greet", "async_greet"],
        )
        self.assertEqual(chunks[1].docstring, "Return a friendly message.")
        self.assertEqual(chunks[2].docstring, "Greets users.")
        self.assertEqual(chunks[3].docstring, "Build a greeting.")
        self.assertEqual(chunks[4].docstring, "Build an async greeting.")
        self.assertIn("import os", chunks[0].source_code)
        self.assertIn('print(helper("world"))', chunks[-1].source_code)


if __name__ == "__main__":
    unittest.main()
