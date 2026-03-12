.PHONY: install test test-headless test-parallel test-parallel-selenium test-safari pw-test pw-headed pw-parallel check clean help lint format

SITE     ?= internet
BROWSER  ?= chrome
PYTEST   := python -m pytest

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Install project dependencies
	pip install -r requirements.txt

test: ## Run tests (default: chrome, headed)
	$(PYTEST) --site=$(SITE) --browser=$(BROWSER)

test-headless: ## Run tests in headless Chrome
	$(PYTEST) --site=$(SITE) --browser=chrome --headless

test-parallel: ## Run tests in parallel headless Chrome
	$(PYTEST) -n auto --site=$(SITE) --browser=chrome --headless

test-parallel-selenium: ## Run Selenium tests in parallel headless Chrome (exclude Playwright)
	$(PYTEST) -n auto --site=$(SITE) --browser=chrome --headless -m "not playwright"

test-safari: ## Run tests in Safari (serial only)
	$(PYTEST) --site=$(SITE) --browser=safari

pw-test: ## Run Playwright tests (chromium)
	$(PYTEST) tests/playwright -m playwright --pw-browser=chromium

pw-headed: ## Run Playwright tests in headed mode
	$(PYTEST) tests/playwright -m playwright --pw-headed --pw-browser=chromium

pw-parallel: ## Run Playwright tests in parallel
	$(PYTEST) tests/playwright -m playwright -n auto --pw-browser=chromium

lint: ## Run ruff linter
	ruff check .

format: ## Auto-format code with ruff
	ruff format .
	ruff check --fix .

check: ## Run lint and format checks without writing changes
	ruff check .
	ruff format --check .

clean: ## Remove caches and artifacts
	rm -rf __pycache__ .pytest_cache .ruff_cache artifacts/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
