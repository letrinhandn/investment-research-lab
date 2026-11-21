"""Import and gate passed alphas from quant-trading (no training pipeline here)."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import yaml
from irl_core.paths import repo_root

from irl_lab.scaffold import new_plugin


def quant_trading_root() -> Path:
    env = os.environ.get("QT_ROOT") or os.environ.get("QUANT_TRADING_ROOT")
    if not env:
        try:
            from irl_core.settings import get_settings

            settings = get_settings()
            env = settings.qt_root or settings.quant_trading_root
        except Exception:
            env = None
    if env:
        return Path(env).expanduser().resolve()
    sibling = repo_root().parent / "quant-trading"
    if sibling.is_dir():
        return sibling.resolve()
    raise FileNotFoundError(
        "quant-trading root not found. Set QT_ROOT in .env to the local quant-trading path."
    )


def registry_path() -> Path:
    return quant_trading_root() / "artifacts" / "algorithms" / "registry.jsonl"


def latest_runs_by_slug() -> dict[str, dict]:
    path = registry_path()
    if not path.exists():
        raise FileNotFoundError(f"Missing registry: {path}")
    latest: dict[str, dict] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        slug = row.get("slug")
        if not slug:
            continue
        prev = latest.get(slug)
        if prev is None or str(row.get("created_at", "")) >= str(prev.get("created_at", "")):
            latest[slug] = row
    return latest


def _oos(row: dict) -> dict:
    metrics = row.get("metrics") or {}
    oos = metrics.get("oos_metrics") or {}
    return oos if isinstance(oos, dict) else {}


def import_alpha(
    slug: str,
    *,
    status: str = "pass",
    domain: str = "equities",
    copy_equity: bool = True,
) -> Path:
    """Pull one alpha card from quant-trading into alphas/<slug>/ (no training here)."""
    runs = latest_runs_by_slug()
    if slug not in runs:
        raise KeyError(f"Alpha slug not in registry: {slug}")
    row = runs[slug]
    oos = _oos(row)
    dest = repo_root() / "alphas" / slug
    if not dest.exists():
        dest = new_plugin("alpha", slug, domain=domain)
    meta = {
        "name": slug,
        "status": status,
        "domain": domain,
        "source": "quant-trading",
        "source_slug": slug,
        "run_id": row.get("run_id"),
        "created_at": row.get("created_at"),
        "tags": row.get("tags") or [],
        "notes": row.get("notes") or "",
        "metrics": {
            "sharpe": oos.get("sharpe"),
            "ann_return": oos.get("ann_return"),
            "ann_vol": oos.get("ann_vol"),
            "max_drawdown": oos.get("max_drawdown"),
            "total_return": oos.get("total_return"),
            "days": oos.get("days"),
        },
        "description": (row.get("config") or {}).get("description")
        or (row.get("config") or {}).get("display_name")
        or slug,
    }
    (dest / "config.yaml").write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True))
    evidence = dest / "evidence"
    evidence.mkdir(exist_ok=True)
    (evidence / "registry_snapshot.json").write_text(json.dumps(row, indent=2, default=str))
    if copy_equity:
        equity = ((row.get("artifacts") or {}).get("equity_csv")) or ""
        src = Path(equity) if equity else None
        if src and src.exists():
            shutil.copy2(src, evidence / "equity.csv")
    (dest / "README.md").write_text(
        f"# {slug}\n\n"
        f"Imported from quant-trading. Status: `{status}`.\n\n"
        f"Run id: `{meta.get('run_id')}`.\n"
    )
    return dest


def import_alphas(
    slugs: list[str] | None = None,
    *,
    status: str = "pass",
    domain: str = "equities",
    min_sharpe: float | None = None,
    copy_equity: bool = True,
) -> list[Path]:
    """Import many alphas from quant-trading. Default: all latest registry slugs."""
    runs = latest_runs_by_slug()
    chosen = list(slugs) if slugs else sorted(runs.keys())
    out: list[Path] = []
    for slug in chosen:
        if slug not in runs:
            raise KeyError(f"Alpha slug not in registry: {slug}")
        if min_sharpe is not None:
            sharpe = _oos(runs[slug]).get("sharpe")
            try:
                if sharpe is None or float(sharpe) < float(min_sharpe):
                    continue
            except (TypeError, ValueError):
                continue
        out.append(
            import_alpha(
                slug,
                status=status,
                domain=domain,
                copy_equity=copy_equity,
            )
        )
    return out


def load_alpha(slug: str) -> dict:
    path = repo_root() / "alphas" / slug / "config.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Alpha card missing: {path}")
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid alpha config: {path}")
    return data


def assert_alpha_pass(slug: str) -> dict:
    meta = load_alpha(slug)
    status = str(meta.get("status", "")).lower()
    if status != "pass":
        raise PermissionError(
            f"Alpha `{slug}` status is `{status or 'unset'}`. "
            "Only status=pass alphas may open a full report."
        )
    return meta


def list_passed_alphas() -> list[dict]:
    root = repo_root() / "alphas"
    if not root.is_dir():
        return []
    out: list[dict] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith("_"):
            continue
        cfg = child / "config.yaml"
        if not cfg.exists():
            continue
        meta = yaml.safe_load(cfg.read_text()) or {}
        if str(meta.get("status", "")).lower() == "pass":
            out.append(meta if isinstance(meta, dict) else {"name": child.name})
    return out
