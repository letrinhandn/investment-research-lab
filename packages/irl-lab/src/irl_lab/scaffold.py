"""Create new plugins from templates."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml
from irl_core.paths import repo_root

KIND_CONFIG = {
    "alpha": ("alphas", "config.yaml"),
    "report": ("reports", "config.yaml"),
    "memo": ("memos", "config.yaml"),
    "idea": ("ideas", "config.yaml"),
    "watchlist": ("watchlists", "config.yaml"),
    "notebook": ("notebooks", "config.yaml"),
    "paper": ("papers", "config.yaml"),
    "post": ("posts", "config.yaml"),
    "project": ("projects", "config.yaml"),
    "data": ("data", "manifest.yaml"),
    "dataset": ("datasets", "config.yaml"),
}


def new_plugin(kind: str, name: str, domain: str = "general") -> Path:
    if kind not in KIND_CONFIG:
        raise ValueError(f"Unknown kind: {kind}. Choose from {sorted(KIND_CONFIG)}")
    folder, meta_name = KIND_CONFIG[kind]
    root = repo_root()
    slug = name.strip().lower().replace(" ", "-")
    dest = root / folder / slug
    if dest.exists():
        raise FileExistsError(f"Already exists: {dest}")
    template = root / folder / "_template"
    if template.exists():
        shutil.copytree(template, dest)
    else:
        dest.mkdir(parents=True)
    meta_path = dest / meta_name
    meta = {
        "name": slug,
        "status": "draft",
        "domain": domain,
        "description": "",
    }
    if kind == "paper":
        meta.update({"format": "article", "engine": "markdown"})
    if kind == "post":
        meta.update({"channel": "quarto", "format": "html", "status": "draft"})
    if kind == "memo":
        meta.update({"thesis": "", "horizon": ""})
    if kind == "alpha":
        meta.update(
            {
                "status": "candidate",
                "source": "quant-trading",
                "source_slug": slug,
                "metrics": {},
            }
        )
    if kind == "report":
        meta.update(
            {
                "status": "draft",
                "alpha": "",
                "format": "research-report",
                "engine": "markdown",
            }
        )
    if kind == "data":
        meta = {
            "slug": slug,
            "status": "draft",
            "domain": domain,
            "provider": "manual",
            "description": "",
        }
    meta_path.write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True))
    readme = dest / "README.md"
    if not readme.exists():
        readme.write_text(f"# {slug}\n\nDraft {kind} plugin.\n")
    if kind == "project":
        run_py = dest / "run.py"
        if not run_py.exists():
            run_py.write_text(
                'from __future__ import annotations\n\nfrom typing import Any\n\n\n'
                "def run(config: dict[str, Any]) -> int:\n"
                '    print(f"Project: {config.get(\'name\', \'unknown\')}")\n'
                "    return 0\n"
            )
    if kind == "memo":
        body = dest / "memo.md"
        if not body.exists():
            body.write_text(f"# {slug}\n\n## Thesis\n\n## Facts\n\n## Risks\n\n## Decision\n")
    if kind == "idea":
        body = dest / "idea.md"
        if not body.exists():
            body.write_text(f"# {slug}\n\n## Hook\n\n## Questions\n")
    if kind == "watchlist":
        body = dest / "names.csv"
        if not body.exists():
            body.write_text("symbol,note\n")
    if kind == "notebook":
        nb = dest / f"{slug}.ipynb"
        if not nb.exists():
            nb.write_text(
                '{\n "cells": [],\n "metadata": {"kernelspec": '
                '{"display_name": "Python 3", "language": "python", "name": "python3"}},'
                '\n "nbformat": 4,\n "nbformat_minor": 5\n}\n'
            )
    if kind == "post":
        example = dest / "index.qmd.example"
        qmd = dest / "index.qmd"
        if not qmd.exists():
            if example.exists():
                qmd.write_text(
                    example.read_text().replace(
                        'title: "Essay title"', f'title: "{slug}"'
                    )
                )
                example.unlink()
            else:
                qmd.write_text(
                    "---\n"
                    f'title: "{slug}"\n'
                    'description: ""\n'
                    'author: "Le Tri Nhan"\n'
                    "date: today\n"
                    "categories: [markets]\n"
                    "draft: true\n"
                    "---\n\n"
                    f"## {slug}\n\n"
                    "Draft Quarto essay.\n"
                )
        elif example.exists():
            example.unlink()
        old = dest / "draft.md"
        if old.exists():
            old.unlink()
    if kind == "alpha":
        (dest / "evidence").mkdir(exist_ok=True)
    if kind == "report":
        body = dest / "report.md"
        if not body.exists():
            body.write_text(_report_stub(slug))
        (dest / "figures").mkdir(exist_ok=True)
        (dest / "tables").mkdir(exist_ok=True)
    return dest


def _report_stub(slug: str) -> str:
    return (
        f"# {slug}\n\n"
        "## Abstract\n\n"
        "## Alpha under review\n\n"
        "- Source alpha:\n"
        "- Pass gate: yes\n"
        "- Key OOS metrics:\n\n"
        "## Hypothesis\n\n"
        "## Data and sample\n\n"
        "## Method\n\n"
        "## Results\n\n"
        "## Risk and failure modes\n\n"
        "## Decision\n\n"
        "- Deploy / watch / reject:\n"
        "- Next review date:\n"
    )


def new_report_for_alpha(name: str, alpha: str, domain: str = "equities") -> Path:
    """Create a full report only when the linked alpha card is status=pass."""
    from irl_lab.alphas import assert_alpha_pass

    meta_alpha = assert_alpha_pass(alpha)
    dest = new_plugin("report", name, domain=domain)
    cfg_path = dest / "config.yaml"
    cfg = yaml.safe_load(cfg_path.read_text()) or {}
    cfg.update(
        {
            "name": name.strip().lower().replace(" ", "-"),
            "alpha": alpha,
            "status": "draft",
            "domain": domain,
            "alpha_metrics": meta_alpha.get("metrics") or {},
            "format": "research-report",
            "engine": "markdown",
            "description": f"Full report for passed alpha `{alpha}`",
        }
    )
    cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True))
    metrics = meta_alpha.get("metrics") or {}
    report = dest / "report.md"
    report.write_text(
        f"# {cfg['name']}\n\n"
        "## Abstract\n\n"
        f"Research report for passed alpha `{alpha}`.\n\n"
        "## Alpha under review\n\n"
        f"- Source alpha: `{alpha}`\n"
        f"- Pass gate: yes\n"
        f"- Sharpe: {metrics.get('sharpe')}\n"
        f"- Ann return: {metrics.get('ann_return')}\n"
        f"- Ann vol: {metrics.get('ann_vol')}\n"
        f"- Max drawdown: {metrics.get('max_drawdown')}\n"
        f"- Total return: {metrics.get('total_return')}\n"
        f"- OOS days: {metrics.get('days')}\n\n"
        "## Hypothesis\n\n"
        "## Data and sample\n\n"
        "## Method\n\n"
        "## Results\n\n"
        "## Risk and failure modes\n\n"
        "## Decision\n\n"
        "- Deploy / watch / reject:\n"
        "- Next review date:\n"
    )
    (dest / "README.md").write_text(
        f"# {cfg['name']}\n\nFull report linked to passed alpha `{alpha}`.\n"
    )
    return dest


def reports_for_passed_alphas(
    *,
    domain: str = "equities",
    prefix: str = "report-",
) -> list[Path]:
    """Create a full report for each passed alpha that does not already have one linked."""
    from irl_lab.alphas import list_passed_alphas
    from irl_lab.registry import discover

    existing = {str(p.meta.get("alpha") or "") for p in discover("reports")}
    created: list[Path] = []
    for meta in list_passed_alphas():
        slug = str(meta.get("name") or meta.get("source_slug") or "").strip()
        if not slug or slug in existing:
            continue
        name = f"{prefix}{slug}".strip("-")
        created.append(new_report_for_alpha(name, alpha=slug, domain=domain))
    return created


