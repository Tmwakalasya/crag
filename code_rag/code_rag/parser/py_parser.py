"""Python AST chunk extraction built on top of tree-sitter."""

from __future__ import annotations

import ast
from dataclasses import dataclass

from ..models import CodeChunk


@dataclass(frozen=True)
class _DocstringKey:
    chunk_type: str
    name: str
    start_line: int


@dataclass(frozen=True)
class _Span:
    start_byte: int
    end_byte: int


def parse_python_source(file_path: str, source_code: str) -> list[CodeChunk]:
    """Parse Python source code into AST-aligned chunks."""
    parser = _build_python_parser()
    source_bytes = source_code.encode("utf-8")
    tree = parser.parse(source_bytes)
    docstrings = _collect_docstrings(source_code)

    root_node = tree.root_node
    definition_nodes = [
        node for node in root_node.named_children if node.type in _DEFINITION_NODE_TYPES
    ]

    chunks: list[CodeChunk] = []
    global_scope_index = 0
    cursor = 0

    for node in definition_nodes:
        global_chunk = _build_global_scope_chunk(
            file_path=file_path,
            source_code=source_code,
            span=_Span(start_byte=cursor, end_byte=node.start_byte),
            index=global_scope_index,
        )
        if global_chunk is not None:
            chunks.append(global_chunk)
            global_scope_index += 1

        chunks.append(
            _build_definition_chunk(
                file_path=file_path,
                source_bytes=source_bytes,
                node=node,
                docstrings=docstrings,
            )
        )

        if node.type == "class_definition":
            chunks.extend(
                _build_method_chunks(
                    file_path=file_path,
                    source_bytes=source_bytes,
                    class_node=node,
                    docstrings=docstrings,
                )
            )

        cursor = node.end_byte

    trailing_global_chunk = _build_global_scope_chunk(
        file_path=file_path,
        source_code=source_code,
        span=_Span(start_byte=cursor, end_byte=len(source_code.encode("utf-8"))),
        index=global_scope_index,
    )
    if trailing_global_chunk is not None:
        chunks.append(trailing_global_chunk)

    return chunks


_DEFINITION_NODE_TYPES = {"function_definition", "async_function_definition", "class_definition"}


def _build_python_parser():
    import importlib
    import importlib.util

    if (
        importlib.util.find_spec("tree_sitter") is None
        or importlib.util.find_spec("tree_sitter_python") is None
    ):
        raise RuntimeError(
            "tree-sitter and tree-sitter-python are required to parse Python source"
        )

    tree_sitter = importlib.import_module("tree_sitter")
    tree_sitter_python = importlib.import_module("tree_sitter_python")
    Language = tree_sitter.Language
    Parser = tree_sitter.Parser

    language_factory = getattr(tree_sitter_python, "language", None)
    if language_factory is None:
        raise RuntimeError("tree-sitter-python does not expose a language() factory")

    language_capsule = language_factory()
    try:
        language = Language(language_capsule)
    except TypeError:
        language = language_capsule

    try:
        return Parser(language)
    except TypeError:
        parser = Parser()
        if hasattr(parser, "set_language"):
            parser.set_language(language)
        else:
            parser.language = language
        return parser


def _build_definition_chunk(
    file_path: str,
    source_bytes: bytes,
    node,
    docstrings: dict[_DocstringKey, str],
) -> CodeChunk:
    name = _node_name(node, source_bytes)
    start_line, end_line = _line_bounds(node)
    chunk_type = "class" if node.type == "class_definition" else "function"

    return CodeChunk(
        file_path=file_path,
        language="python",
        chunk_type=chunk_type,
        name=name,
        start_line=start_line,
        end_line=end_line,
        source_code=source_bytes[node.start_byte : node.end_byte].decode("utf-8"),
        docstring=docstrings.get(_DocstringKey(chunk_type=chunk_type, name=name, start_line=start_line)),
    )


def _build_method_chunks(
    file_path: str,
    source_bytes: bytes,
    class_node,
    docstrings: dict[_DocstringKey, str],
) -> list[CodeChunk]:
    body_node = class_node.child_by_field_name("body")
    if body_node is None:
        return []

    chunks: list[CodeChunk] = []
    for node in body_node.named_children:
        if node.type not in {"function_definition", "async_function_definition"}:
            continue

        name = _node_name(node, source_bytes)
        start_line, end_line = _line_bounds(node)
        chunks.append(
            CodeChunk(
                file_path=file_path,
                language="python",
                chunk_type="method",
                name=name,
                start_line=start_line,
                end_line=end_line,
                source_code=source_bytes[node.start_byte : node.end_byte].decode("utf-8"),
                docstring=docstrings.get(
                    _DocstringKey(chunk_type="method", name=name, start_line=start_line)
                ),
            )
        )

    return chunks


def _build_global_scope_chunk(
    file_path: str,
    source_code: str,
    span: _Span,
    index: int,
) -> CodeChunk | None:
    start_line, end_line, text = _slice_text(source_code, span)
    if not text.strip():
        return None

    return CodeChunk(
        file_path=file_path,
        language="python",
        chunk_type="global_scope",
        name=f"global_scope_{index}",
        start_line=start_line,
        end_line=end_line,
        source_code=text,
        docstring=None,
    )


def _slice_text(source_code: str, span: _Span) -> tuple[int, int, str]:
    source_bytes = source_code.encode("utf-8")
    text = source_bytes[span.start_byte : span.end_byte].decode("utf-8")
    start_line = source_bytes[: span.start_byte].count(b"\n") + 1
    end_line = start_line + text.count("\n")
    return start_line, end_line, text


def _line_bounds(node) -> tuple[int, int]:
    start_line = node.start_point[0] + 1
    end_line = node.end_point[0] + 1
    return start_line, end_line


def _node_name(node, source_bytes: bytes) -> str:
    name_node = node.child_by_field_name("name")
    if name_node is None:
        return "<anonymous>"
    return source_bytes[name_node.start_byte : name_node.end_byte].decode("utf-8")


def _collect_docstrings(source_code: str) -> dict[_DocstringKey, str]:
    parsed = ast.parse(source_code)
    docstrings: dict[_DocstringKey, str] = {}

    for node in parsed.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            docstring = ast.get_docstring(node)
            if docstring:
                docstrings[_DocstringKey("function", node.name, node.lineno)] = docstring
        elif isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node)
            if docstring:
                docstrings[_DocstringKey("class", node.name, node.lineno)] = docstring
            for inner_node in node.body:
                if isinstance(inner_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    inner_docstring = ast.get_docstring(inner_node)
                    if inner_docstring:
                        docstrings[
                            _DocstringKey("method", inner_node.name, inner_node.lineno)
                        ] = inner_docstring

    return docstrings
