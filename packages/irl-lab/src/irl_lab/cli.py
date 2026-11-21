"""irl CLI — single entry point."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from irl_lab.registry import PLUGIN_KINDS, discover
from irl_lab.scaffold import new_plugin, new_report_for_alpha

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
    try:
        from irl_lab.alphas import quant_trading_root, registry_path

        qt = quant_trading_root()
        reg = registry_path()
        console.print(f"QT_ROOT: {qt} ({'ok' if qt.is_dir() else 'missing'})")
        console.print(f"QT registry: {reg} ({'ok' if reg.exists() else 'missing'})")
    except FileNotFoundError as exc:
        console.print(f"QT_ROOT: {exc}")


@app.command("list")
def list_plugins(kind: str | None = typer.Argument(None)) -> None:
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
    alpha: str | None = typer.Option(
        None, "--alpha", "-a", help="Required for report: passed alpha slug"
    ),
) -> None:
    if kind == "report":
        if not alpha:
            raise typer.BadParameter("report requires --alpha <passed-slug>")
        path = new_report_for_alpha(name, alpha=alpha, domain=domain)
    else:
        path = new_plugin(kind, name, domain=domain)
    console.print(f"Created {path}")


@app.command("import-alpha")
def import_alpha_cmd(
    slug: str = typer.Argument(..., help="Algorithm slug from quant-trading registry"),
    domain: str = typer.Option("equities", "--domain", "-d"),
    status: str = typer.Option(
        "pass",
        "--status",
        "-s",
        help="Card status after import (pass unlocks full reports)",
    ),
    no_equity: bool = typer.Option(False, "--no-equity", help="Skip copying equity.csv"),
) -> None:
    from irl_lab.alphas import import_alpha

    path = import_alpha(slug, status=status, domain=domain, copy_equity=not no_equity)
    console.print(f"Imported alpha card: {path} (status={status})")


@app.command("import-alphas")
def import_alphas_cmd(
    slugs: list[str] | None = typer.Argument(
        None, help="Slugs to import; default = all in registry"
    ),
    domain: str = typer.Option("equities", "--domain", "-d"),
    status: str = typer.Option("pass", "--status", "-s"),
    min_sharpe: float | None = typer.Option(
        None, "--min-sharpe", help="Only import latest runs with OOS Sharpe >= this"
    ),
    no_equity: bool = typer.Option(False, "--no-equity"),
) -> None:
    from irl_lab.alphas import import_alphas

    paths = import_alphas(
        slugs,
        status=status,
        domain=domain,
        min_sharpe=min_sharpe,
        copy_equity=not no_equity,
    )
    console.print(f"Imported {len(paths)} alpha card(s)")
    for p in paths:
        console.print(f"  {p}")


@app.command("list-passed")
def list_passed_cmd() -> None:
    from irl_lab.alphas import list_passed_alphas

    rows = list_passed_alphas()
    table = Table(title="Passed alphas (report-eligible)")
    table.add_column("slug")
    table.add_column("sharpe")
    table.add_column("ann_return")
    table.add_column("max_dd")
    table.add_column("source")
    for meta in rows:
        metrics = meta.get("metrics") or {}
        table.add_row(
            str(meta.get("name") or meta.get("source_slug") or ""),
            str(metrics.get("sharpe", "")),
            str(metrics.get("ann_return", "")),
            str(metrics.get("max_drawdown", "")),
            str(meta.get("source", "")),
        )
    console.print(table)
    console.print(f"Total: {len(rows)}")


@app.command("new-report")
def new_report_cmd(
    name: str = typer.Argument(..., help="Report slug"),
    alpha: str = typer.Option(..., "--alpha", "-a", help="Passed alpha slug"),
    domain: str = typer.Option("equities", "--domain", "-d"),
) -> None:
    try:
        path = new_report_for_alpha(name, alpha=alpha, domain=domain)
    except (FileNotFoundError, PermissionError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc
    console.print(f"Created full report: {path}")


@app.command("reports-for-passed")
def reports_for_passed_cmd(
    domain: str = typer.Option("equities", "--domain", "-d"),
    prefix: str = typer.Option("report-", "--prefix", help="Report slug prefix"),
) -> None:
    """Scaffold a full report for every passed alpha that does not already have one."""
    from irl_lab.alphas import list_passed_alphas
    from irl_lab.scaffold import reports_for_passed_alphas

    created = reports_for_passed_alphas(domain=domain, prefix=prefix)
    if not created:
        n = len(list_passed_alphas())
        console.print(f"No new reports. Passed alphas: {n}")
        return
    console.print(f"Created {len(created)} report(s)")
    for p in created:
        console.print(f"  {p}")


if __name__ == "__main__":
    app()
