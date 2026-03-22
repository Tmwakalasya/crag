# code-rag

`code-rag` (or `crag`) is a local retrieval-augmented generation CLI for exploring source code repositories. It ingests a codebase, parses files into logical code chunks, stores those chunks in a local vector database, and answers architecture questions using only the indexed code context.

The core design goal is to be **structure-aware**. Instead of chopping files into arbitrary character windows, `code-rag` uses AST-oriented parsing so functions, classes, methods, and top-level module regions are preserved as coherent retrieval units.

---

## Table of Contents

1. [What this project does](#what-this-project-does)
2. [Current status](#current-status)
3. [Why AST-aware chunking matters](#why-ast-aware-chunking-matters)
4. [Architecture overview](#architecture-overview)
5. [Repository layout](#repository-layout)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [CLI usage](#cli-usage)
9. [Typical workflow](#typical-workflow)
10. [How ingestion works](#how-ingestion-works)
11. [How retrieval and answer generation work](#how-retrieval-and-answer-generation-work)
12. [Data model reference](#data-model-reference)
13. [Current implementation notes](#current-implementation-notes)
14. [Running tests](#running-tests)
15. [Troubleshooting](#troubleshooting)
16. [Limitations](#limitations)
17. [Planned improvements](#planned-improvements)
18. [Development notes](#development-notes)

---

## What this project does

At a high level, `code-rag` supports four major stages:

1. **Crawl** a repository and find supported source files.
2. **Parse** each file into logical `CodeChunk` records.
3. **Index** those chunks into a persistent local ChromaDB collection.
4. **Retrieve and answer** natural-language questions against the indexed code.

Today, the implemented system supports:

- Python repository ingestion
- Python AST-aware chunking using `tree-sitter`
- Persistent local storage in ChromaDB
- Local deterministic embeddings for ingestion and retrieval
- Question answering over indexed chunks
- Multiple answer-generation paths:
  - Google Gemini when `GOOGLE_API_KEY` is configured
  - Ollama when explicitly configured
  - a grounded local fallback summary when no external provider is configured

---

## Current status

This repository currently contains the implementation for the Phase 1 through Phase 4 plan from the original technical specification.

### Implemented subsystems

- **CLI layer** for `ingest` and `ask`
- **Configuration helpers** for DB, retrieval, and provider settings
- **Shared Pydantic models** for code chunks and query results
- **Parser engine** with Python routing
- **Python parser** based on `tree-sitter` plus docstring extraction using `ast`
- **Repository crawler** with ignore rules and binary-file filtering
- **Local ChromaDB integration** with deterministic local embeddings
- **Retriever/search layer** for top-k code chunk lookup
- **Generator layer** for prompt construction and answer generation
- **Automated tests** for crawler, DB helpers, parser, search, and generation fallback behavior

### What is stable today

The following user flows work end-to-end:

- ingesting a Python repository into a persistent local ChromaDB database
- querying indexed chunks with `crag ask`
- generating a fallback grounded answer when no external LLM provider is configured

### What is still evolving

The project is functional, but still intentionally early-stage. The largest areas still open for improvement are:

- additional language support beyond Python
- stronger retrieval quality and reranking
- richer answer synthesis and citation formatting
- more ergonomic packaging and distribution
- broader automated test coverage

---

## Why AST-aware chunking matters

A naive RAG pipeline often splits source code by character count, token count, or line count. That creates several problems:

- a function may be split in half across multiple chunks
- class definitions may lose important method context
- global module configuration may be separated from the code that depends on it
- retrieval results may contain incomplete logic fragments

`code-rag` takes a different approach:

- top-level functions remain intact
- classes remain intact
- methods are also extracted as separate chunks
- top-level non-definition module content is preserved as `global_scope`

This improves retrieval quality because the vector store is populated with semantically meaningful units rather than arbitrary slices of text.

---

## Architecture overview

`code-rag` is organized around a simple pipeline:

```text
Repository files
    -> crawler
    -> parser engine
    -> language-specific parser
    -> CodeChunk models
    -> ChromaDB persistence
    -> vector search
    -> prompt construction
    -> answer generation
```

### Pipeline stages

#### 1. Crawler
The crawler walks the target directory recursively and skips known irrelevant folders such as:

- `.git`
- `.idea`
- `.venv`
- `venv`
- `node_modules`
- `__pycache__`

It also filters out binary files and unsupported file extensions before parsing begins.

#### 2. Parser
The parser engine routes a file to the correct language-specific parser based on extension. Right now, `.py` files are supported.

The Python parser extracts:

- `function`
- `class`
- `method`
- `global_scope`

It also records:

- file path
- language
- name
- line range
- exact source code
- optional docstring

#### 3. Indexer
Each `CodeChunk` is stored in ChromaDB with:

- `source_code` as the main document text
- metadata such as `file_path`, `name`, `chunk_type`, and line numbers
- a stable hash-based chunk ID

The current implementation uses a **deterministic local hash embedding function** so ingestion does not require downloading an embedding model from the network.

#### 4. Retriever
For a user question, the retriever performs a vector similarity search against the indexed collection and returns the most relevant chunks.

#### 5. Generator
The generator builds a grounded prompt that includes:

- a system instruction
- the user’s natural-language question
- retrieved code chunks with metadata and source

Then it chooses one of these paths:

1. Gemini, if `GOOGLE_API_KEY` is present
2. Ollama, if explicitly configured
3. a grounded local fallback summary if no provider is available

---

## Repository layout

```text
code_rag/
├── README.md
├── requirements.txt
├── tests/
│   ├── test_crawler.py
│   ├── test_db.py
│   ├── test_generator.py
│   ├── test_py_parser.py
│   └── test_search.py
└── code_rag/
    ├── __init__.py
    ├── config.py
    ├── main.py
    ├── models.py
    ├── indexer/
    │   ├── __init__.py
    │   ├── crawler.py
    │   └── db.py
    ├── parser/
    │   ├── __init__.py
    │   ├── engine.py
    │   └── py_parser.py
    └── retriever/
        ├── __init__.py
        ├── generator.py
        └── search.py
```

### Module responsibilities

#### `code_rag/main.py`
Defines the Typer CLI commands:

- `ingest DIRECTORY_PATH`
- `ask QUERY_STRING`

#### `code_rag/config.py`
Holds environment-aware configuration helpers for:

- database path
- collection name
- retrieval depth
- Gemini model name
- Ollama host/model
- Google API key lookup

#### `code_rag/models.py`
Defines shared Pydantic models:

- `CodeChunk`
- `QueryResult`

#### `code_rag/parser/engine.py`
Routes files to the correct parser by language.

#### `code_rag/parser/py_parser.py`
Uses `tree-sitter` to parse Python into logical chunks and `ast` to extract docstrings.

#### `code_rag/indexer/crawler.py`
Walks the repository, applies ignore rules, and selects supported files.

#### `code_rag/indexer/db.py`
Handles ChromaDB collection creation, local embedding, metadata shaping, and chunk ingestion.

#### `code_rag/retriever/search.py`
Queries the vector store and converts retrieved records back into `CodeChunk` objects.

#### `code_rag/retriever/generator.py`
Builds prompts and produces final answers using Gemini, Ollama, or a fallback summary.

---

## Installation

### Prerequisites

- Python 3.11+ is the target runtime from the spec, though some local environments may also work with 3.10 depending on installed dependencies
- a working virtual environment is strongly recommended

### Basic setup

```bash
cd code_rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Optional provider setup

If you want Gemini-backed synthesis:

```bash
export GOOGLE_API_KEY="your-api-key"
export CODE_RAG_GEMINI_MODEL="gemini-2.5-flash"
```

If you want Ollama-backed synthesis:

```bash
export CODE_RAG_OLLAMA_MODEL="qwen2.5-coder"
export OLLAMA_HOST="http://localhost:11434"
```

If neither is configured, `crag ask` will still work by returning a grounded fallback summary derived from the retrieved chunks.

---

## Configuration

The following environment variables are supported.

| Variable | Purpose | Default |
|---|---|---|
| `CODE_RAG_DB_PATH` | Path to the local persistent ChromaDB directory | `~/.code_rag_db` |
| `CODE_RAG_COLLECTION` | ChromaDB collection name | `code_chunks` |
| `CODE_RAG_TOP_K` | Default number of chunks to retrieve | `5` |
| `GOOGLE_API_KEY` | Enables Gemini generation | unset |
| `CODE_RAG_GEMINI_MODEL` | Gemini model name | `gemini-2.5-flash` |
| `CODE_RAG_OLLAMA_MODEL` | Enables/selects Ollama model | `qwen2.5-coder` |
| `OLLAMA_HOST` | Ollama host URL | `http://localhost:11434` |

### Configuration behavior notes

- If `CODE_RAG_DB_PATH` is not set, data is stored under `~/.code_rag_db`.
- If `CODE_RAG_TOP_K` is not set, `ask` retrieves five chunks by default.
- Gemini is only used when `GOOGLE_API_KEY` is present.
- Ollama is only used when explicitly configured through environment variables.
- If neither provider path is active, the local fallback answer path is used.

---

## CLI usage

### Ingest a repository

```bash
python -m code_rag.main ingest /path/to/repository
```

Example:

```bash
python -m code_rag.main ingest .
```

Expected behavior:

- the repository is crawled
- supported Python files are parsed into chunks
- chunks are embedded with the local deterministic embedding function
- chunks are stored in the configured ChromaDB collection
- a summary table is printed showing file and chunk counts

### Ask a question

```bash
python -m code_rag.main ask "Where is the CLI entry point defined?"
```

You can also override retrieval depth:

```bash
python -m code_rag.main ask "How does ingestion work?" --top-k 8
```

Expected behavior:

- the vector store is queried for relevant chunks
- an answer is generated using the configured provider path
- a fallback grounded summary is used if no provider is configured
- a table of referenced chunks is printed after the answer

---

## Typical workflow

A normal local workflow looks like this:

```bash
cd code_rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m code_rag.main ingest .
python -m code_rag.main ask "Where is repository crawling implemented?"
python -m code_rag.main ask "How are chunks stored in the database?"
```

If you later change the codebase significantly, re-run ingestion to refresh the indexed collection.

---

## How ingestion works

When you run:

```bash
python -m code_rag.main ingest SOME_DIRECTORY
```

this happens internally:

1. The directory path is validated.
2. The crawler gathers supported files.
3. Each file is parsed into `CodeChunk` objects.
4. Each chunk receives:
   - a stable ID
   - a metadata record
   - its `source_code` as the stored document
5. Chunks are upserted into ChromaDB.
6. A summary is printed to the terminal.

### Chunk metadata currently stored

Each chunk persists metadata for:

- `file_path`
- `language`
- `chunk_type`
- `name`
- `start_line`
- `end_line`
- optional `docstring`

### Why local embeddings are used

By default, Chroma may try to use an embedding path that requires downloading a model. This project instead provides a deterministic local hash embedding function so indexing stays self-contained and works in restricted environments.

---

## How retrieval and answer generation work

When you run:

```bash
python -m code_rag.main ask "How does the parser work?"
```

this happens internally:

1. The retriever queries the configured ChromaDB collection.
2. The top-k matching chunks are reconstructed as `CodeChunk` models.
3. A grounded prompt is built from:
   - a system instruction
   - the user question
   - retrieved code chunks and their metadata
4. The generator selects an answer path:
   - Gemini if configured
   - Ollama if explicitly configured
   - local fallback summary otherwise
5. The answer and referenced chunks are printed.

### Fallback mode

Fallback mode is intentionally simple and conservative. It does **not** attempt to hallucinate architectural conclusions. Instead, it summarizes the retrieved context and returns the most relevant excerpts so the user still gets grounded output even without an external LLM.

---

## Data model reference

### `CodeChunk`

A logical unit of code extracted from the repository.

Fields:

- `file_path`: source file path
- `language`: language name, currently `python`
- `chunk_type`: one of `function`, `class`, `method`, or `global_scope`
- `name`: chunk name
- `start_line`: first line in the original file
- `end_line`: last line in the original file
- `source_code`: exact extracted code text
- `docstring`: optional extracted documentation string

### `QueryResult`

The result returned after answering a question.

Fields:

- `answer`: generated or fallback response text
- `referenced_chunks`: list of code chunks used for the answer

---

## Current implementation notes

### Language support

At the moment, the ingestion pipeline only supports Python files.

The parser engine is structured so additional languages can be added later without rewriting the rest of the system.

### Retrieval quality

The current embedding function is intentionally lightweight and deterministic. It is ideal for:

- local development
- offline-friendly behavior
- avoiding large model downloads during indexing

It is **not** expected to outperform modern learned embedding models on semantic retrieval quality.

### Provider selection

Provider selection is intentionally simple:

- use Gemini if `GOOGLE_API_KEY` exists
- otherwise use Ollama if explicitly configured
- otherwise use fallback mode

This keeps the codepath easy to reason about and avoids accidental network behavior when no provider is intended.

---

## Running tests

Run the full test suite with:

```bash
python -m unittest discover -s tests -v
```

### Current tests

- `test_crawler.py` validates ignore rules and binary filtering
- `test_db.py` validates chunk metadata, chunk IDs, and deterministic embeddings
- `test_search.py` validates search result reconstruction
- `test_generator.py` validates prompt generation and fallback behavior
- `test_py_parser.py` validates Python chunk extraction and docstring capture

### Parser test behavior

The parser test depends on `tree_sitter` and `tree_sitter_python`. In environments where those packages are missing, the parser test is designed to skip rather than fail the whole suite.

---

## Troubleshooting

### `ask` returns “No indexed code chunks matched the query”

Possible causes:

- you have not run `ingest` yet
- you ingested a different repository path than the one you intended to query
- you changed `CODE_RAG_DB_PATH` or `CODE_RAG_COLLECTION`
- your query is too narrow for the current embedding approach

Try:

```bash
python -m code_rag.main ingest .
python -m code_rag.main ask "broad summary of the CLI architecture"
```

### Chroma prints telemetry warnings

Some environments may emit non-fatal telemetry warnings from Chroma. If ingestion and retrieval still complete successfully, those warnings are noisy but not typically fatal to local usage.

### Ollama does not answer

Make sure both are true:

- Ollama is running locally
- you explicitly configured either `CODE_RAG_OLLAMA_MODEL` or `OLLAMA_HOST`

### Gemini does not answer

Make sure:

- `GOOGLE_API_KEY` is set
- the selected model name is valid for your account/environment
- outbound network access is allowed

### Retrieval results are not ideal

This is expected for some queries with the current local hash embedding. If retrieval quality matters more than strict offline behavior, a stronger embedding function would be the next major improvement.

---

## Limitations

Current limitations include:

- Python is the only supported language
- retrieval quality is bounded by the lightweight local embedding function
- chunk ranking does not yet include reranking or hybrid search
- answers do not yet include richer inline citations in the generated prose
- the fallback answer path is intentionally conservative and not a substitute for a real model
- packaging and distribution are still minimal

---

## Planned improvements

Potential next steps include:

- Go parser implementation
- richer chunk metadata and symbol relationships
- better embeddings or configurable embedding backends
- hybrid lexical + vector retrieval
- reranking of retrieved chunks
- better answer formatting and citations
- collection maintenance operations such as reset or selective re-indexing
- packaged CLI installation entry points
- more end-to-end integration tests

---

## Development notes

### Useful commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

Ingest the local repository:

```bash
python -m code_rag.main ingest .
```

Ask a question:

```bash
python -m code_rag.main ask "How is ingestion implemented?"
```

### Suggested development flow

1. modify parser, indexer, or retriever logic
2. run tests
3. re-ingest the repository if indexing-related behavior changed
4. run `ask` against a few realistic architectural questions
5. iterate on prompt/retrieval quality

---

## Summary

`code-rag` is now a complete local prototype for AST-aware codebase exploration:

- it ingests Python repositories
- stores logical code chunks locally
- retrieves relevant chunks for natural-language questions
- and produces grounded answers with either external providers or a built-in fallback path

It is intentionally compact and hackable, with a clear path toward stronger parsing, retrieval, and answer-generation capabilities over time.
