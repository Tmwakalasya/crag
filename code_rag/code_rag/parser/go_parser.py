"""Go AST chunk extraction built on top of tree-sitter."""

from __future__ import annotations

from ..models import CodeChunk


def parse_go_source(file_path: str, source_code: str) -> list[CodeChunk]:
    """Parse Go source code into AST-aligned chunks."""
    parser = _build_go_parser()
    source_bytes = source_code.encode("utf-8")
    tree = parser.parse(source_bytes)

    root_node = tree.root_node
    chunks: list[CodeChunk] = []
    global_scope_index = 0
    cursor = 0

    definition_nodes = [
        node
        for node in root_node.named_children
        if node.type in _DEFINITION_NODE_TYPES
    ]

    for node in definition_nodes:
        global_chunk = _build_global_scope_chunk(
            file_path=file_path,
            source_code=source_code,
            start_byte=cursor,
            end_byte=node.start_byte,
            index=global_scope_index,
        )
        if global_chunk is not None:
            chunks.append(global_chunk)
            global_scope_index += 1

        if node.type == "function_declaration":
            chunks.append(_build_function_chunk(file_path, source_bytes, node))
        elif node.type == "method_declaration":
            chunks.append(_build_method_chunk(file_path, source_bytes, node))
        elif node.type == "type_declaration":
            chunks.extend(_build_type_chunks(file_path, source_bytes, node))

        cursor = node.end_byte

    trailing = _build_global_scope_chunk(
        file_path=file_path,
        source_code=source_code,
        start_byte=cursor,
        end_byte=len(source_code.encode("utf-8")),
        index=global_scope_index,
    )
    if trailing is not None:
        chunks.append(trailing)

    return chunks


_DEFINITION_NODE_TYPES = {
    "function_declaration",
    "method_declaration",
    "type_declaration",
}


def _build_go_parser():
    import importlib
    import importlib.util

    if (
        importlib.util.find_spec("tree_sitter") is None
        or importlib.util.find_spec("tree_sitter_go") is None
    ):
        raise RuntimeError(
            "tree-sitter and tree-sitter-go are required to parse Go source"
        )

    tree_sitter = importlib.import_module("tree_sitter")
    tree_sitter_go = importlib.import_module("tree_sitter_go")
    Language = tree_sitter.Language
    Parser = tree_sitter.Parser

    language_factory = getattr(tree_sitter_go, "language", None)
    if language_factory is None:
        raise RuntimeError("tree-sitter-go does not expose a language() factory")

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


def _build_function_chunk(
    file_path: str, source_bytes: bytes, node
) -> CodeChunk:
    name = _node_name(node, source_bytes)
    start_line, end_line = _line_bounds(node)
    doc = _leading_comment(node, source_bytes)
    return CodeChunk(
        file_path=file_path,
        language="go",
        chunk_type="function",
        name=name,
        start_line=start_line,
        end_line=end_line,
        source_code=source_bytes[node.start_byte : node.end_byte].decode("utf-8"),
        docstring=doc,
    )


def _build_method_chunk(
    file_path: str, source_bytes: bytes, node
) -> CodeChunk:
    name = _node_name(node, source_bytes)
    receiver = _receiver_type(node, source_bytes)
    if receiver:
        name = f"{receiver}.{name}"
    start_line, end_line = _line_bounds(node)
    doc = _leading_comment(node, source_bytes)
    return CodeChunk(
        file_path=file_path,
        language="go",
        chunk_type="method",
        name=name,
        start_line=start_line,
        end_line=end_line,
        source_code=source_bytes[node.start_byte : node.end_byte].decode("utf-8"),
        docstring=doc,
    )


def _build_type_chunks(
    file_path: str, source_bytes: bytes, node
) -> list[CodeChunk]:
    """Extract type spec chunks from a type_declaration node."""
    chunks: list[CodeChunk] = []
    for child in node.named_children:
        if child.type == "type_spec":
            name = _node_name(child, source_bytes)
            start_line, end_line = _line_bounds(node)
            doc = _leading_comment(node, source_bytes)
            chunks.append(
                CodeChunk(
                    file_path=file_path,
                    language="go",
                    chunk_type="type",
                    name=name,
                    start_line=start_line,
                    end_line=end_line,
                    source_code=source_bytes[node.start_byte : node.end_byte].decode("utf-8"),
                    docstring=doc,
                )
            )
    return chunks


def _build_global_scope_chunk(
    file_path: str,
    source_code: str,
    start_byte: int,
    end_byte: int,
    index: int,
) -> CodeChunk | None:
    source_bytes = source_code.encode("utf-8")
    text = source_bytes[start_byte:end_byte].decode("utf-8")
    if not text.strip():
        return None
    start_line = source_bytes[:start_byte].count(b"\n") + 1
    end_line = start_line + text.count("\n")
    return CodeChunk(
        file_path=file_path,
        language="go",
        chunk_type="global_scope",
        name=f"global_scope_{index}",
        start_line=start_line,
        end_line=end_line,
        source_code=text,
        docstring=None,
    )


def _line_bounds(node) -> tuple[int, int]:
    return node.start_point[0] + 1, node.end_point[0] + 1


def _node_name(node, source_bytes: bytes) -> str:
    name_node = node.child_by_field_name("name")
    if name_node is None:
        return "<anonymous>"
    return source_bytes[name_node.start_byte : name_node.end_byte].decode("utf-8")


def _receiver_type(node, source_bytes: bytes) -> str | None:
    """Extract the receiver type name from a method_declaration."""
    params = node.child_by_field_name("receiver")
    if params is None:
        return None
    for child in params.named_children:
        if child.type == "parameter_declaration":
            type_node = child.child_by_field_name("type")
            if type_node is not None:
                raw = source_bytes[type_node.start_byte : type_node.end_byte].decode("utf-8")
                return raw.lstrip("*")
    return None


def _leading_comment(node, source_bytes: bytes) -> str | None:
    """Collect consecutive // comment lines immediately above the node."""
    prev = node.prev_named_sibling
    if prev is None or prev.type != "comment":
        return None

    comments: list[str] = []
    current = prev
    while current is not None and current.type == "comment":
        line = source_bytes[current.start_byte : current.end_byte].decode("utf-8")
        line = line.lstrip("/").strip()
        comments.append(line)
        current = current.prev_named_sibling

    comments.reverse()
    return "\n".join(comments) if comments else None
