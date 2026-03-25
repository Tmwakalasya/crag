# crag — Code RAG

A local, AST-aware retrieval-augmented generation CLI for exploring codebases. Ingest a repository, ask questions in natural language, get answers grounded in your actual code.

## Why crag?

Most code search tools split files by character count, breaking functions in half and losing context. **crag** uses tree-sitter AST parsing to preserve functions, classes, and methods as intact retrieval units — so you always get complete, meaningful code in results.

**Zero ML required for core functionality.** Ingestion and retrieval use a deterministic hash-based embedding — no model downloads, no GPU, no network calls. LLM-powered answer generation is optional and supports multiple cloud providers.

## Quick Start

```bash
# Install core (no ML dependencies)
cd code_rag
pip install -e .

# Ingest a repository
crag ingest /path/to/your/project

# Ask questions (works immediately with fallback mode)
crag ask "Where is the CLI entry point?"

# For LLM-powered answers, pick any provider you already use:
pip install -e ".[openai]"       # or .[anthropic], .[gemini], .[ollama], .[all]
export OPENAI_API_KEY="sk-..."   # set your preferred provider's key
crag ask "How does the parser work?"
```

## LLM Providers

crag tries providers in this order and uses the first one that is both installed and configured:

| Provider | Install | Environment Variable |
|---|---|---|
| Google Gemini | `pip install -e ".[gemini]"` | `GOOGLE_API_KEY` |
| OpenAI | `pip install -e ".[openai]"` | `OPENAI_API_KEY` |
| Anthropic | `pip install -e ".[anthropic]"` | `ANTHROPIC_API_KEY` |
| Ollama (local) | `pip install -e ".[ollama]"` | `CODE_RAG_OLLAMA_MODEL` or `OLLAMA_HOST` |
| Fallback | *(built-in)* | *(none needed)* |

The **fallback mode** returns the most relevant code chunks with excerpts — no hallucination, no network calls. It's useful on its own for code search even without any LLM.

### Model Configuration

| Variable | Default |
|---|---|
| `CODE_RAG_GEMINI_MODEL` | `gemini-2.5-flash` |
| `CODE_RAG_OPENAI_MODEL` | `gpt-4o-mini` |
| `CODE_RAG_ANTHROPIC_MODEL` | `claude-sonnet-4-20250514` |
| `CODE_RAG_OLLAMA_MODEL` | `qwen2.5-coder` |
| `OLLAMA_HOST` | `http://localhost:11434` |

## CLI Usage

### `crag ingest <directory>`

Crawl and index a repository. Re-running replaces stale data for that repo.

```bash
crag ingest .
crag ingest /path/to/project
```

### `crag ask <question>`

Query indexed code and get a grounded answer.

```bash
crag ask "How does ingestion work?"
crag ask "Where are the Pydantic models defined?" --top-k 10
crag ask "Show me all CLI commands" --directory /path/to/project
crag ask "Compare parser implementations" --all-repos
```

| Flag | Description | Default |
|---|---|---|
| `--top-k` | Number of chunks to retrieve | `5` |
| `--directory` / `-d` | Repository to search | `.` |
| `--all-repos` | Search all ingested repositories | `false` |

## How It Works

```
Repository → Crawler → tree-sitter Parser → CodeChunks → ChromaDB → Vector Search → LLM Answer
```

1. **Crawler** walks the repo, skipping `.git`, `node_modules`, `__pycache__`, etc.
2. **Parser** uses tree-sitter to extract functions, classes, methods, and global scope as intact chunks with metadata (file path, line range, docstring).
3. **Indexer** embeds chunks using a deterministic SHA1-based hash function (256-dim vectors) and stores them in a local ChromaDB database.
4. **Retriever** performs vector similarity search to find the top-k relevant chunks.
5. **Generator** builds a grounded prompt and sends it to the configured LLM, or returns a fallback summary.

### Why Deterministic Embeddings?

The hash-based embedding function:
- Works offline with zero setup
- Produces identical results every time (deterministic)
- Requires no model downloads or GPU
- Keeps the core install under 100MB

The tradeoff is lower semantic retrieval quality compared to learned embeddings. For most code search tasks on a single repository, keyword-level matching works surprisingly well.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `CODE_RAG_DB_PATH` | ChromaDB storage directory | `~/.code_rag_db` |
| `CODE_RAG_COLLECTION` | Collection name | `code_chunks` |
| `CODE_RAG_TOP_K` | Default retrieval depth | `5` |

## Supported Languages

- **Python** — full AST-aware chunking via tree-sitter
- Go parser support is prepared but not yet implemented

## Project Structure

```
code_rag/
├── code_rag/
│   ├── main.py              # CLI commands (ingest, ask)
│   ├── config.py            # Environment-based configuration
│   ├── models.py            # CodeChunk, QueryResult (Pydantic)
│   ├── parser/
│   │   ├── engine.py        # Language detection & routing
│   │   └── py_parser.py     # Python AST parser (tree-sitter)
│   ├── indexer/
│   │   ├── crawler.py       # Repository walker with ignore rules
│   │   └── db.py            # ChromaDB + hash embedding
│   └── retriever/
│       ├── search.py        # Vector similarity search
│       └── generator.py     # Multi-provider answer generation
├── tests/
├── pyproject.toml
└── requirements.txt
```

## Development

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e ".[all]"

# Run tests
python -m unittest discover -s tests -v

# Dev workflow
crag ingest .
crag ask "How is ingestion implemented?"
```

## Troubleshooting

**"No indexed code chunks matched the query"** — Run `crag ingest` first, or broaden your question.

**Ollama not answering** — Ensure Ollama is running and you've set `CODE_RAG_OLLAMA_MODEL` or `OLLAMA_HOST`.

**Poor retrieval results** — Expected for some queries with hash embeddings. Try more specific keywords or increase `--top-k`.

## Limitations

- Python is the only fully supported language
- Hash-based embeddings trade semantic quality for determinism and portability
- No reranking or hybrid search yet
- Fallback mode returns excerpts, not synthesized answers
