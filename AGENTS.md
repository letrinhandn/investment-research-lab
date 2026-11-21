# AGENTS.md — Investment Research Lab

Read this first. This repo is an infinite knowledge vault for investment research.

## Mental model

```
ALPHAS (import only)              REPORTS (gated)
alphas/<slug>/                    reports/<slug>/
  config.yaml  status=pass|...      config.yaml  alpha: <slug>
  evidence/                         report.md
                                    figures/ tables/

MEMOS              IDEAS             WATCHLISTS
memos/<slug>/      ideas/<slug>/     watchlists/<slug>/
  memo.md            idea.md           names.csv

NOTEBOOKS          PAPERS            POSTS (Quarto)       PROJECTS
notebooks/<slug>/  papers/<slug>/    posts/<slug>/        projects/<slug>/
                                       index.qmd

DATA               DATASETS
data/<slug>/       datasets/<slug>/
```

One CLI: `python -m irl_lab.cli` (alias `irl` after `uv sync`)

**No alpha training pipeline here.** Import from quant-trading (`QT_ROOT`), then write reports only when `alphas/<slug>/config.yaml` has `status: pass`.

## Commands

```bash
make setup
make doctor
make list

make import-alpha NAME=regime-hmm-rl DOMAIN=equities
make import-alphas MIN_SHARPE=1.0 STATUS=pass
make list-passed
make new-report NAME=2026-11-regime-hmm ALPHA=regime-hmm-rl
make reports-for-passed

make new-memo NAME=2026-11-vn-banks DOMAIN=vietnam
make new-idea NAME=stablecoin-float DOMAIN=crypto
make new-watchlist NAME=vn30-core DOMAIN=equities
make new-notebook NAME=earnings-quality DOMAIN=equities
make new-paper NAME=informal-markets-note DOMAIN=vietnam
make new-post NAME=how-i-size-risk DOMAIN=general
make new-project NAME=factor-screen DOMAIN=equities
make new-data NAME=dnse-quotes DOMAIN=equities
make new-dataset NAME=vn-bank-panel DOMAIN=vietnam

make preview          # Quarto site
make render
make publish          # GitHub Pages when ready
```

Posts publish via Quarto (`posts/<slug>/index.qmd`), not Substack. See `docs/quarto.md`.

## Directory contract

| Path | Purpose | Required |
|------|---------|----------|
| `alphas/<slug>/` | Imported alpha card | `config.yaml`, `evidence/` |
| `reports/<slug>/` | Full report for a passed alpha | `config.yaml`, `report.md` |
| `memos/<slug>/` | Investment thesis memo | `config.yaml`, `memo.md` |
| `ideas/<slug>/` | Early idea card | `config.yaml`, `idea.md` |
| `watchlists/<slug>/` | Names under review | `config.yaml`, `names.csv` |
| `notebooks/<slug>/` | Analysis notebooks | `config.yaml` |
| `papers/<slug>/` | Academic paper | `config.yaml` |
| `posts/<slug>/` | Quarto essay | `config.yaml`, `index.qmd` |
| `projects/<slug>/` | Runnable research | `config.yaml`, `run.py` |
| `data/<slug>/` | Data source | `manifest.yaml` |
| `datasets/<slug>/` | Curated pack | `config.yaml` |

Slug rules: kebab-case, lowercase, no leading `_`. Prefer `YYYY-MM-slug` for memos and reports.

## Report gate

- `irl new-report` / `make new-report` refuse unless the linked alpha has `status: pass`.
- `reports-for-passed` scaffolds one report per passed alpha that is not already linked.
- Import default status is `pass` so a deliberate import unlocks reporting; use `STATUS=candidate` if you only want a card.

## Artifacts

Use `irl_core.paths`. Outputs under `artifacts/` (gitignored).

Set `QT_ROOT` in `.env` when quant-trading is not at `../quant-trading`.

## Anti-patterns

- Hardcode `artifacts/` paths
- Commit brokerage secrets or filled personal account dumps
- Train / search / backtest alphas here (use quant-trading)
- Open a full report for non-pass alphas
- Mix pricing-theory notebooks here (use Quant Theory Lab)
- Treat this vault as a live order router (use trading production stack)
