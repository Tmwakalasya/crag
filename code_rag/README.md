# code-rag

`code-rag` (or `crag`) is a local retrieval-augmented generation CLI for exploring software repositories. It is designed to parse source code into logical AST-based chunks, index them into a local vector database, and answer architecture questions grounded in those chunks.

## Status

This repository currently contains Phase 1 and Phase 2 foundation work from the technical specification:

- dependency definitions in `requirements.txt`
- a Typer-based CLI scaffold in `code_rag/main.py`
- configuration helpers in `code_rag/config.py`
- shared Pydantic models in `code_rag/models.py`
- a parser engine in `code_rag/parser/engine.py`
- a tree-sitter-backed Python parser in `code_rag/parser/py_parser.py`
- a standalone parser test in `tests/test_py_parser.py`
- package skeletons for the indexer and retriever modules

## Quick start

```bash
cd code_rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m code_rag.main --help
python -m unittest discover -s tests -v
```

## Planned commands

- `crag ingest DIRECTORY_PATH`
- `crag ask QUERY_STRING`

The CLI commands are wired as entry points today. The parser implementation now exists for Python files, while the indexing and retrieval flows are still scheduled for later phases.
