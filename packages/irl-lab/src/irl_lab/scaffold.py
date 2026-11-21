"""Create new plugins from templates."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from irl_core.paths import repo_root

KIND_CONFIG = {
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
        meta.update({"channel": "substack", "status": "draft"})
    if kind == "memo":
        meta.update({"thesis": "", "horizon": ""})
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
        draft = dest / "draft.md"
        if not draft.exists():
            draft.write_text(f"# {slug}\n\nDraft essay.\n")
    return dest
