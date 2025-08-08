# This file is part of the tschm/.config-templates repository
# (https://github.com/tschm/.config-templates).
#
# Colors for pretty output
BLUE := \033[36m
BOLD := \033[1m
GREEN := \033[32m
RESET := \033[0m


SOURCE_FOLDER := src
TESTS_FOLDER := tests
MARIMO_FOLDER := book/marimo
OPTIONS ?=

.DEFAULT_GOAL := help

.PHONY: help verify install fmt lint deptry test build check marimo clean docs debug

##@ Development Setup

uv:
	@printf "$(BLUE)Creating virtual environment...$(RESET)\n"
	@curl -LsSf https://astral.sh/uv/install.sh | sh

install: uv ## Install all dependencies using uv
	@printf "$(BLUE)Installing dependencies...$(RESET)\n"
	@uv venv --clear --python 3.12
	@if [ -f "pyproject.toml" ]; then \
		uv sync --all-extras --frozen; \
	else \
		printf "$(BLUE)No pyproject.toml found, skipping uv sync$(RESET)\n"; \
	fi

##@ Code Quality

fmt: uv ## Run code formatters only
	@printf "$(BLUE)Running formatters...$(RESET)\n"
	@uvx ruff format .

lint: uv ## Run linters only
	@printf "$(BLUE)Running linters...$(RESET)\n"
	@uvx pre-commit run --all-files

check: lint fmt test ## Run all checks (lint and conditionally test)
	@printf "$(GREEN)All checks passed!$(RESET)\n"

deptry: uv ## Run deptry (use OPTIONS="--your-options" to pass options)
	@printf "$(BLUE)Running deptry...$(RESET)\n"
	@if [ ! -f "pyproject.toml" ]; then \
		printf "$(BLUE)No pyproject.toml found, skipping deptry$(RESET)\n"; \
	elif [ -z "$(SOURCE_FOLDER)" ]; then \
		printf "$(BLUE)No valid source folder structure found, skipping deptry$(RESET)\n"; \
	else \
		uvx deptry $(SOURCE_FOLDER) $(OPTIONS); \
	fi

##@ Testing

test: install
	@printf "$(BLUE)Running tests...$(RESET)\n"
	@if [ ! -f "README.md" ]; then \
		printf "$(BLUE)No README.md file found, skipping tests$(RESET)\n"; \
	elif [ -z "$(SOURCE_FOLDER)" ] || [ -z "$(TESTS_FOLDER)" ]; then \
		printf "$(BLUE)No valid source folder structure found, skipping tests$(RESET)\n"; \
	else \
		echo "$$GITHUB_REPOSITORY"; \
		uv pip install pytest pytest-cov pytest-html python-dotenv; \
		mkdir -p _tests/html-coverage _tests/html-report; \
		uv run pytest $(TESTS_FOLDER) \
			--cov=$(SOURCE_FOLDER) \
			--cov-report=term \
			--cov-report=html:_tests/html-coverage \
			--html=_tests/html-report/report.html; \
	fi

##@ Building

build: install ## Build the package
	@printf "$(BLUE)Building package...$(RESET)\n"
	@if [ -f "pyproject.toml" ]; then \
		uv pip install hatch; \
		uv run hatch build; \
	else \
		printf "$(BLUE)No pyproject.toml found, skipping build$(RESET)\n"; \
	fi

##@ Documentation

docs: install ## Build documentation
	@printf "$(BLUE)Building documentation...$(RESET)\n"
	@if [ ! -f "pyproject.toml" ]; then \
		printf "$(BLUE)No pyproject.toml found, skipping docs$(RESET)\n"; \
	elif [ -z "$(SOURCE_FOLDER)" ]; then \
		printf "$(BLUE)No valid source folder structure found, skipping docs$(RESET)\n"; \
	else \
		uv pip install pdoc; \
		{ \
			uv run pdoc -o _pdoc $(SOURCE_FOLDER); \
			if command -v xdg-open >/dev/null 2>&1; then \
				xdg-open "_pdoc/index.html"; \
			elif command -v open >/dev/null 2>&1; then \
				open "_pdoc/index.html"; \
			else \
				echo "Documentation generated. Open pdoc/index.html manually"; \
			fi; \
		}; \
	fi

##@ Cleanup

clean: ## Clean generated files and directories
	@printf "$(BLUE)Cleaning project...$(RESET)\n"
	@rm -rf dist build *.egg-info .coverage .pytest_cache _tests .venv
	@if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then \
		printf "$(BLUE)Cleaning git-tracked files...$(RESET)\n"; \
		git clean -d -X -f; \
		printf "$(BLUE)Removing local branches with no remote counterpart...$(RESET)\n"; \
		if git remote | grep -q .; then \
			git fetch -p; \
			git branch -vv | grep ': gone]' | awk '{print $$1}' | xargs -r git branch -D 2>/dev/null || true; \
		else \
			printf "$(BLUE)No git remotes found, skipping branch cleanup$(RESET)\n"; \
		fi; \
	else \
		printf "$(BLUE)Not in a git repository, skipping git cleanup$(RESET)\n"; \
	fi

##@ Marimo

marimo: install ## Start a Marimo server
	@printf "$(BLUE)Start Marimo server with $(MARIMO_FOLDER)...$(RESET)\n"
	@uv pip install marimo
	@uv run marimo edit $(MARIMO_FOLDER)

##@ Help

help: ## Display this help message
	@printf "$(BOLD)Usage:$(RESET)\n"
	@printf "  make $(BLUE)<target>$(RESET)\n\n"
	@printf "$(BOLD)Targets:$(RESET)\n"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  $(BLUE)%-15s$(RESET) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BOLD)%s$(RESET)\n", substr($$0, 5) }' $(MAKEFILE_LIST)
