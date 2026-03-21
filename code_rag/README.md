# code-rag

`code-rag` (or `crag`) is a local retrieval-augmented generation CLI for exploring software repositories. It is designed to parse source code into logical AST-based chunks, index them into a local vector database, and answer architecture questions grounded in those chunks.

## Status

This repository currently contains the Phase 1 foundation work from the technical specification:

- dependency definitions in `requirements.txt`
- a Typer-based CLI scaffold in `code_rag/main.py`
- configuration helpers in `code_rag/config.py`
- shared Pydantic models in `code_rag/models.py`
- package skeletons for the parser, indexer, and retriever modules

## Quick start

```bash
cd code_rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m code_rag.main --help
```

## Planned commands

- `crag ingest DIRECTORY_PATH`
- `crag ask QUERY_STRING`

Both commands are wired as CLI entry points today and intentionally raise a helpful message until the later phases are implemented.
