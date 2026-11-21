# AGENTS.md — Investment Research Lab

Read this first. This repo is an infinite knowledge vault for investment research.

## Mental model

```
MEMOS              IDEAS             WATCHLISTS
memos/<slug>/      ideas/<slug>/     watchlists/<slug>/
  memo.md            idea.md           names.csv

NOTEBOOKS          PAPERS            POSTS (Substack)     PROJECTS
notebooks/<slug>/  papers/<slug>/    posts/<slug>/        projects/<slug>/

DATA               DATASETS
data/<slug>/       datasets/<slug>/
```

One CLI: `python -m irl_lab.cli` (alias `irl` after `uv sync`)

## Commands

```bash
make setup
make doctor
make list

make new-memo NAME=2026-11-vn-banks DOMAIN=vietnam
make new-idea NAME=stablecoin-float DOMAIN=crypto
make new-watchlist NAME=vn30-core DOMAIN=equities
make new-notebook NAME=earnings-quality DOMAIN=equities
make new-paper NAME=informal-markets-note DOMAIN=vietnam
make new-post NAME=how-i-size-risk DOMAIN=general
make new-project NAME=factor-screen DOMAIN=equities
make new-data NAME=dnse-quotes DOMAIN=equities
make new-dataset NAME=vn-bank-panel DOMAIN=vietnam
```

## Directory contract

| Path | Purpose | Required |
|------|---------|----------|
| `memos/<slug>/` | Investment thesis memo | `config.yaml`, `memo.md` |
| `ideas/<slug>/` | Early idea card | `config.yaml`, `idea.md` |
| `watchlists/<slug>/` | Names under review | `config.yaml`, `names.csv` |
| `notebooks/<slug>/` | Analysis notebooks | `config.yaml` |
| `papers/<slug>/` | Academic paper | `config.yaml` |
| `posts/<slug>/` | Substack / essay | `config.yaml`, `draft.md` |
| `projects/<slug>/` | Runnable research | `config.yaml`, `run.py` |
| `data/<slug>/` | Data source | `manifest.yaml` |
| `datasets/<slug>/` | Curated pack | `config.yaml` |

Slug rules: kebab-case, lowercase, no leading `_`. Prefer `YYYY-MM-slug` for memos.

## Artifacts

Use `irl_core.paths`. Outputs under `artifacts/` (gitignored).

## Anti-patterns

- Hardcode `artifacts/` paths
- Commit brokerage secrets or filled personal account dumps
- Mix pricing-theory notebooks here (use Quant Theory Lab)
- Treat this vault as a live order router (use trading production stack)
