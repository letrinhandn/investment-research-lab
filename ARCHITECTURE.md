# Architecture

## Overview

```
Makefile + irl CLI
        |
   filesystem plugins          packages (uv workspace)
   memos ideas watchlists      irl-core
   notebooks papers posts      irl-lab
   projects data datasets
        |
   artifacts/ (gitignored)
```

## Plugin pattern

Every unit of knowledge is a folder plugin. Discovery is filesystem-first. `lab/registry.yaml` is optional metadata.

## Scaling

- Infinite plugins via `make new-*`
- Idea to memo to paper/post without leaving the vault
- Data manifests and curated datasets grow independently
- Shared agent contract in `AGENTS.md`

## Boundaries

- This lab: investment theses, ideas, watchlists, applied research writing
- Quant Theory Lab: pricing theory and model notebooks
- quant-trading / Terminal Trade: production systems and market UIs
