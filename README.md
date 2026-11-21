# Investment Research Lab

Infinite knowledge vault for **investment research**.

Memos, ideas, watchlists, Jupyter analysis, academic papers, Quarto essays, data sources, curated datasets, research projects, plus **passed alphas imported from quant-trading** and full research reports. Scale by adding plugins. No hard limit.

This vault does **not** train or run an alpha pipeline. Alpha search stays in quant-trading. Here you pull cards that clear your gate and write the report. Essays publish via Quarto, not Substack.

Author: Le Tri Nhan  
Visibility: private

## Mental model

```
QUANT-TRADING (engine)     IRL ALPHAS              IRL REPORTS
registry.jsonl      -->    alphas/<slug>/   -->    reports/<slug>/
                           status=pass only        full write-up
```

```
MEMOS / IDEAS / WATCHLISTS     NOTEBOOKS / PAPERS / POSTS     DATA / DATASETS / PROJECTS
decision pipeline              writing and analysis           evidence layer
```

## Quick start

```bash
make setup
cp docs/env.example .env   # set QT_ROOT if quant-trading is not a sibling folder
make doctor
make list
```

### Import passed alphas and open reports

```bash
# Pull one alpha card from quant-trading (default status=pass)
make import-alpha NAME=regime-hmm-rl DOMAIN=equities

# Pull several, or all latest registry slugs with a Sharpe floor
make import-alphas NAME=regime-hmm-rl,std-vnindex
make import-alphas MIN_SHARPE=1.0 STATUS=pass

make list-passed

# Full report only if the alpha card is status=pass
make new-report NAME=2026-11-regime-hmm ALPHA=regime-hmm-rl DOMAIN=equities

# Or scaffold a report for every passed alpha that still lacks one
make reports-for-passed
```

### Publish essays (Quarto, not Substack)

```bash
make new-post NAME=position-sizing
# edit posts/<slug>/index.qmd  → set draft: false
make preview
make render
make publish   # GitHub Pages when ready
```

See [docs/quarto.md](docs/quarto.md).

### Add other knowledge

```bash
make new-memo NAME=2026-11-vn-banks DOMAIN=vietnam
make new-idea NAME=stablecoin-float DOMAIN=crypto
make new-watchlist NAME=vn30-core DOMAIN=equities
make new-notebook NAME=earnings-quality DOMAIN=equities
make new-paper NAME=local-markets-note DOMAIN=vietnam
make new-post NAME=position-sizing DOMAIN=general
make new-project NAME=factor-screen DOMAIN=equities
make new-data NAME=macro-fred DOMAIN=macro
make new-dataset NAME=vn-bank-panel DOMAIN=vietnam
```

## Layout

```text
alphas/       Imported alpha cards (from quant-trading)
reports/      Full research reports (gated on status=pass)
memos/        Investment theses
ideas/        Early idea cards
watchlists/   Names under review
notebooks/    Analysis Jupyter
papers/       Academic writing
posts/        Quarto essays (index.qmd)
projects/     Runnable research
data/         Data source manifests
datasets/     Curated packs
packages/     irl-core, irl-lab
lab/          Registry
_quarto.yml   Quarto website
_site/        Built site (gitignored)
artifacts/    Local outputs (gitignored)
```

## Related vaults

- [Quant Theory Lab](https://github.com/letrinhandn/quant-theory-lab)
- [Terminal Trade](https://github.com/letrinhandn/Terminal-Trade)

## License

MIT. Private research. Not investment advice.

> AI agents: read [AGENTS.md](AGENTS.md) first.
