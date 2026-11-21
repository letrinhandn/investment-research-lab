.PHONY: help setup sync doctor list \
        import-alpha import-alphas list-passed new-report reports-for-passed \
        new-memo new-idea new-watchlist new-notebook new-paper new-post \
        new-project new-data new-dataset \
        preview render publish quarto-doctor \
        lint test

REPO := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
IRL := cd $(REPO) && uv run --python 3.12 python -m irl_lab.cli
QUARTO ?= $(shell command -v quarto 2>/dev/null || echo $(HOME)/.local/bin/quarto)

NAME ?=
ALPHA ?=
DOMAIN ?= general
STATUS ?= pass
MIN_SHARPE ?=
PREFIX ?= report-

help:
	@echo "Investment Research Lab"
	@echo ""
	@echo "  make setup                       Install workspace"
	@echo "  make doctor                      Health check"
	@echo "  make list                        List all plugins"
	@echo "  make import-alpha NAME=x         Pull one alpha from quant-trading"
	@echo "  make import-alphas               Pull alphas (optional NAME=a,b MIN_SHARPE=1.0)"
	@echo "  make list-passed                 List report-eligible alphas"
	@echo "  make new-report NAME=x ALPHA=y   Full report (ALPHA must be status=pass)"
	@echo "  make reports-for-passed          Scaffold reports for all passed alphas"
	@echo "  make new-memo NAME=x             Investment memo"
	@echo "  make new-idea NAME=x             Idea card"
	@echo "  make new-watchlist NAME=x        Watchlist"
	@echo "  make new-notebook NAME=x         Analysis notebook"
	@echo "  make new-paper NAME=x            Academic paper"
	@echo "  make new-post NAME=x             Quarto essay"
	@echo "  make new-project NAME=x          Research project"
	@echo "  make new-data NAME=x             Data source"
	@echo "  make new-dataset NAME=x          Curated dataset"
	@echo "  make preview                     Quarto live preview"
	@echo "  make render                      Build Quarto site to _site/"
	@echo "  make publish                     Publish to GitHub Pages (when ready)"
	@echo "  make quarto-doctor               Quarto install check"
	@echo "  make lint                        Ruff"
	@echo "  make test                        Pytest"

setup sync:
	cd $(REPO) && uv sync --all-groups

doctor:
	$(IRL) doctor

list:
	$(IRL) list

import-alpha:
	@test -n "$(NAME)" || (echo "NAME= required (quant-trading slug)" && exit 1)
	$(IRL) import-alpha $(NAME) --domain $(DOMAIN) --status $(STATUS)

import-alphas:
ifeq ($(strip $(NAME)),)
	$(IRL) import-alphas --domain $(DOMAIN) --status $(STATUS) $(if $(MIN_SHARPE),--min-sharpe $(MIN_SHARPE),)
else
	$(IRL) import-alphas $(subst $(comma), ,$(NAME)) --domain $(DOMAIN) --status $(STATUS) $(if $(MIN_SHARPE),--min-sharpe $(MIN_SHARPE),)
endif

list-passed:
	$(IRL) list-passed

new-report:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	@test -n "$(ALPHA)" || (echo "ALPHA= required (passed alpha slug)" && exit 1)
	$(IRL) new-report $(NAME) --alpha $(ALPHA) --domain $(DOMAIN)

reports-for-passed:
	$(IRL) reports-for-passed --domain $(DOMAIN) --prefix $(PREFIX)

new-memo:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(IRL) new memo $(NAME) --domain $(DOMAIN)

new-idea:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(IRL) new idea $(NAME) --domain $(DOMAIN)

new-watchlist:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(IRL) new watchlist $(NAME) --domain $(DOMAIN)

new-notebook:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(IRL) new notebook $(NAME) --domain $(DOMAIN)

new-paper:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(IRL) new paper $(NAME) --domain $(DOMAIN)

new-post:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(IRL) new post $(NAME) --domain $(DOMAIN)

new-project:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(IRL) new project $(NAME) --domain $(DOMAIN)

new-data:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(IRL) new data $(NAME) --domain $(DOMAIN)

new-dataset:
	@test -n "$(NAME)" || (echo "NAME= required" && exit 1)
	$(IRL) new dataset $(NAME) --domain $(DOMAIN)

quarto-doctor:
	@$(QUARTO) --version
	cd $(REPO) && $(QUARTO) check

preview:
	cd $(REPO) && $(QUARTO) preview

render:
	cd $(REPO) && $(QUARTO) render

publish:
	cd $(REPO) && $(QUARTO) publish gh-pages --no-prompt

lint:
	cd $(REPO) && uv run ruff check packages

test:
	cd $(REPO) && uv run pytest

comma := ,
