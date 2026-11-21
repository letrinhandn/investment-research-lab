"""irl CLI — single entry point."""

from __future__ import annotations

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from irl_lab.registry import PLUGIN_KINDS, discover
from irl_lab.scaffold import new_plugin

app = typer.Typer(help="Investment Research Lab CLI", no_args_is_help=True)
console = Console()


@app.command("doctor")
def doctor() -> None:
    from irl_core.paths import artifacts, repo_root

    root = repo_root()
    console.print(f"IRL_ROOT: {root}")
    console.print(f"artifacts: {artifacts()} ({'ok' if artifacts().exists() else 'missing'})")
    for kind in PLUGIN_KINDS:
        console.print(f"  {kind}: {len(discover(kind))}")


@app.command("list")
def list_plugins(kind: Optional[str] = typer.Argument(None)) -> None:
    plugins = discover(kind)
    table = Table(title="Investment Research Lab plugins")
    table.add_column("kind")
    table.add_column("slug")
    table.add_column("status")
    table.add_column("domain")
    for p in plugins:
        table.add_row(
            p.kind,
            p.slug,
            str(p.meta.get("status", "")),
            str(p.meta.get("domain", "")),
        )
    console.print(table)


@app.command("new")
def new_cmd(
    kind: str = typer.Argument(...),
    name: str = typer.Argument(...),
    domain: str = typer.Option("general", "--domain", "-d"),
) -> None:
    path = new_plugin(kind, name, domain=domain)
    console.print(f"Created {path}")


if __name__ == "__main__":
    app()
