"""Typer CLI entry points for code-rag."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from .config import default_db_path

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
    console.print(
        Panel.fit(
            (
                "[bold yellow]Phase 1 scaffold[/bold yellow]\n"
                f"Ingest is not implemented yet. Target repository: [cyan]{resolved_path}[/cyan]\n"
                f"Configured database path: [cyan]{default_db_path()}[/cyan]"
            ),
            title="crag ingest",
        )
    )
    raise typer.Exit(code=1)


@app.command()
def ask(query_string: str) -> None:
    """Ask an architecture question grounded in indexed code chunks."""
    console.print(
        Panel.fit(
            (
                "[bold yellow]Phase 1 scaffold[/bold yellow]\n"
                f"Ask is not implemented yet. Query received: [cyan]{query_string}[/cyan]\n"
                f"Configured database path: [cyan]{default_db_path()}[/cyan]"
            ),
            title="crag ask",
        )
    )
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
