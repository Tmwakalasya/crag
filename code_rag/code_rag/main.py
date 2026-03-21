"""Typer CLI entry points for code-rag."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .config import db_path

app = typer.Typer(
    add_completion=False,
    help="Local RAG CLI for AST-aware codebase exploration.",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main() -> None:
    """Run the code-rag CLI."""


@app.command()
def ingest(directory_path: Path) -> None:
    """Ingest a local repository into the persistent vector store."""
    resolved_path = directory_path.expanduser().resolve()
    if not resolved_path.exists() or not resolved_path.is_dir():
        raise typer.BadParameter(f"Directory does not exist: {resolved_path}")

    from .indexer.crawler import crawl_code_chunks, iter_source_files
    from .indexer.db import ingest_chunks

    source_files = iter_source_files(resolved_path)
    chunks = crawl_code_chunks(resolved_path)
    stored_chunks = ingest_chunks(chunks)

    summary = Table.grid(padding=(0, 2))
    summary.add_row("Repository", str(resolved_path))
    summary.add_row("Database path", str(db_path()))
    summary.add_row("Source files", str(len(source_files)))
    summary.add_row("Chunks indexed", str(stored_chunks))

    console.print(Panel.fit(summary, title="crag ingest"))


@app.command()
def ask(query_string: str) -> None:
    """Ask an architecture question grounded in indexed code chunks."""
    console.print(
        Panel.fit(
            (
                "[bold yellow]Phase 4 pending[/bold yellow]\n"
                f"Ask is not implemented yet. Query received: [cyan]{query_string}[/cyan]\n"
                f"Configured database path: [cyan]{db_path()}[/cyan]"
            ),
            title="crag ask",
        )
    )
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
