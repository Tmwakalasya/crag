# code-rag

`code-rag` (or `crag`) is a local retrieval-augmented generation CLI for exploring software repositories. It is designed to parse source code into logical AST-based chunks, index them into a local vector database, and answer architecture questions grounded in those chunks.

## Status

This repository currently contains Phase 1 through Phase 3 work from the technical specification:

- dependency definitions in `requirements.txt`
- a Typer-based CLI scaffold in `code_rag/main.py`
- configuration helpers in `code_rag/config.py`
- shared Pydantic models in `code_rag/models.py`
- a parser engine in `code_rag/parser/engine.py`
- a tree-sitter-backed Python parser in `code_rag/parser/py_parser.py`
- a repository crawler in `code_rag/indexer/crawler.py`
- local ChromaDB persistence helpers in `code_rag/indexer/db.py`
- standalone tests for the parser, crawler, and DB helpers in `tests/`
- a package skeleton for the retriever module

## Quick start

```bash
cd code_rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m code_rag.main ingest .
python -m unittest discover -s tests -v
```

## Planned commands

- `crag ingest DIRECTORY_PATH`
- `crag ask QUERY_STRING`

`crag ingest` is now wired to crawl Python files, parse them into logical chunks, and persist them into a local ChromaDB collection. `crag ask` remains scheduled for the retrieval/generation phase.
