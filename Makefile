.PHONY: install test test-headless test-parallel test-parallel-headed test-parallel-selenium test-parallel-selenium-headed test-safari selenium-geolocation selenium-geolocation-headed playwright-geolocation playwright-geolocation-headed pw-test pw-headed pw-parallel pw-parallel-headed framework-parallel-headed selenium-parallel-headed playwright-parallel-headed check clean help lint format

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

framework-parallel-headed: ## Run framework tests in parallel headed Chrome
	$(PYTEST) -n auto --site=$(SITE) --browser=chrome

test-parallel-headed: framework-parallel-headed

test-parallel-selenium: ## Run Selenium tests in parallel headless Chrome (exclude Playwright)
	$(PYTEST) -n auto --site=$(SITE) --browser=chrome --headless -m "not playwright"

selenium-parallel-headed: ## Run Selenium tests in parallel headed Chrome (exclude Playwright)
	$(PYTEST) -n auto --site=$(SITE) --browser=chrome -m "not playwright"

test-parallel-selenium-headed: selenium-parallel-headed

test-safari: ## Run tests in Safari (serial only)
	$(PYTEST) --site=$(SITE) --browser=safari

selenium-geolocation: ## Run Selenium geolocation tests (headless Chrome)
	$(PYTEST) tests/internet/test_geolocation.py --site=$(SITE) --browser=chrome --headless -m "not playwright"

selenium-geolocation-headed: ## Run Selenium geolocation tests (headed Chrome)
	$(PYTEST) tests/internet/test_geolocation.py --site=$(SITE) --browser=chrome -m "not playwright"

playwright-geolocation: ## Run Playwright geolocation tests (headless Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py -m playwright --pw-browser=chromium

playwright-geolocation-headed: ## Run Playwright geolocation tests (headed Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py -m playwright --pw-headed --pw-browser=chromium

pw-test: ## Run Playwright tests (chromium)
	$(PYTEST) tests/playwright -m playwright --pw-browser=chromium

pw-headed: ## Run Playwright tests in headed mode
	$(PYTEST) tests/playwright -m playwright --pw-headed --pw-browser=chromium

pw-parallel: ## Run Playwright tests in parallel
	$(PYTEST) tests/playwright -m playwright -n auto --pw-browser=chromium

playwright-parallel-headed: ## Run Playwright tests in parallel headed mode
	$(PYTEST) tests/playwright -m playwright -n auto --pw-headed --pw-browser=chromium

pw-parallel-headed: playwright-parallel-headed

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
