# Quarto publishing

Posts are Quarto essays under `posts/<slug>/index.qmd`. This replaces Substack.

Memos, alphas, and full reports stay in the vault. Only essays under `posts/` go on the Quarto site.

## Workflow

```bash
make new-post NAME=position-sizing DOMAIN=general
# edit posts/position-sizing/index.qmd
# set draft: false when ready

make preview    # local site
make render     # build _site/
make publish    # GitHub Pages (first time needs gh auth + Pages enabled)
```

## Front matter

```yaml
---
title: "How I size risk"
description: "..."
author: "Le Tri Nhan"
date: 2026-11-21
categories: [markets, risk]
draft: false
---
```

## Publish target

Default: GitHub Pages via `quarto publish gh-pages`.

1. Repo Settings → Pages → Source: `gh-pages` branch
2. `make publish`
3. Site URL: `https://letrinhandn.github.io/investment-research-lab`

Alternative: [Quarto Pub](https://quartopub.com) with `quarto publish quarto-pub`.

## Install

Quarto CLI is expected on `PATH`, or at `~/.local/bin/quarto`.

Env templates live in `docs/env.example` (not `.env.example`) so Quarto does not treat empty keys as required.
