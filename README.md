# Investment Research Lab

Infinite knowledge vault for **investment research**.

Memos, ideas, watchlists, Jupyter analysis, academic papers, Substack essays, data sources, curated datasets, and research projects. Scale by adding plugins. No hard limit.

Author: Le Tri Nhan  
Visibility: private

## Mental model

```
MEMOS / IDEAS / WATCHLISTS     NOTEBOOKS / PAPERS / POSTS     DATA / DATASETS / PROJECTS
decision pipeline              writing and analysis           evidence layer
```

## Quick start

```bash
make setup
cp .env.example .env
make doctor
make list
```

### Add knowledge

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
memos/        Investment theses
ideas/        Early idea cards
watchlists/   Names under review
notebooks/    Analysis Jupyter
papers/       Academic writing
posts/        Substack and essays
projects/     Runnable research
data/         Data source manifests
datasets/     Curated packs
packages/     irl-core, irl-lab
lab/          Registry
artifacts/    Local outputs (gitignored)
```

## Related vaults

- [Quant Theory Lab](https://github.com/letrinhandn/quant-theory-lab)
- [Terminal Trade](https://github.com/letrinhandn/Terminal-Trade)

## License

MIT. Private research. Not investment advice.

> AI agents: read [AGENTS.md](AGENTS.md) first.
