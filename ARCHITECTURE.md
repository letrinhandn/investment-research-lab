# Architecture

## Overview

```
Makefile + irl CLI
        |
   filesystem plugins                 packages (uv workspace)
   alphas reports                     irl-core
   memos ideas watchlists             irl-lab  (import + report gate)
   notebooks papers posts
   projects data datasets
        |
   artifacts/ (gitignored)

quant-trading artifacts/algorithms/registry.jsonl
        |
   irl import-alpha / import-alphas   (copy card + evidence only)
```

## Publishing

Quarto website at repo root (`_quarto.yml`). Essay listing reads `posts/*/index.qmd`. Build to `_site/`. Publish with `make publish` (GitHub Pages). Memos/alphas/reports stay vault-only unless you promote content into a post.

## Plugin pattern

Every unit of knowledge is a folder plugin. Discovery is filesystem-first. `lab/registry.yaml` is optional metadata.

## Alphas and reports

1. Alpha search and evaluation stay in quant-trading.
2. IRL imports a card into `alphas/<slug>/` (config + evidence snapshot).
3. Full reports live under `reports/` and require `status: pass` on the alpha card.
4. Report scaffolds prefill Abstract / Alpha under review / Hypothesis / Data / Method / Results / Risk / Decision.

## Scaling

- Infinite plugins via `make new-*` and `make import-*`
- Idea to memo to paper/post without leaving the vault
- Passed alphas to full reports without a second research repo
- Data manifests and curated datasets grow independently
- Shared agent contract in `AGENTS.md`

## Boundaries

- This lab: investment theses, imported alphas, full reports, watchlists, applied research writing
- Quant Theory Lab: pricing theory and model notebooks
- quant-trading / Terminal Trade: alpha engine, production systems, market UIs
