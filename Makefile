.PHONY: help setup sync doctor list \
        new-memo new-idea new-watchlist new-notebook new-paper new-post \
        new-project new-data new-dataset \
        lint test

REPO := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
IRL := cd $(REPO) && uv run --python 3.12 python -m irl_lab.cli

NAME ?=
DOMAIN ?= general

help:
	@echo "Investment Research Lab"
	@echo ""
	@echo "  make setup                  Install workspace"
	@echo "  make doctor                 Health check"
	@echo "  make list                   List all plugins"
	@echo "  make new-memo NAME=x        Investment memo"
	@echo "  make new-idea NAME=x        Idea card"
	@echo "  make new-watchlist NAME=x   Watchlist"
	@echo "  make new-notebook NAME=x    Analysis notebook"
	@echo "  make new-paper NAME=x       Academic paper"
	@echo "  make new-post NAME=x        Substack / essay"
	@echo "  make new-project NAME=x     Research project"
	@echo "  make new-data NAME=x        Data source"
	@echo "  make new-dataset NAME=x     Curated dataset"
	@echo "  make lint                   Ruff"
	@echo "  make test                   Pytest"

setup sync:
	cd $(REPO) && uv sync --all-groups

doctor:
	$(IRL) doctor

list:
	$(IRL) list

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

lint:
	cd $(REPO) && uv run ruff check packages

test:
	cd $(REPO) && uv run pytest
