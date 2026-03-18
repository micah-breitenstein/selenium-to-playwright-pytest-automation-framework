.PHONY: install test test-headless test-parallel test-parallel-headed test-parallel-selenium test-parallel-selenium-headed test-safari selenium-geolocation selenium-geolocation-headed selenium-geolocation-parks selenium-geolocation-parks-headed playwright-geolocation playwright-geolocation-headed playwright-geolocation-parks playwright-geolocation-parks-headed playwright-geolocation-parks-multistop playwright-geolocation-parks-multistop-headed playwright-geolocation-target playwright-geolocation-target-headed playwright-geolocation-target-park playwright-geolocation-target-park-headed pw-test pw-headed pw-parallel pw-parallel-headed framework-parallel-headed selenium-parallel-headed playwright-parallel-headed check clean help lint format

SITE     ?= internet
BROWSER  ?= chrome
NAV_WAIT_MS ?= 0
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

selenium-geolocation-parks: ## Run Selenium nearby-park navigation test (headless Chrome)
	$(PYTEST) tests/internet/test_geolocation.py::test_geolocation_navigates_google_maps_top_10_named_parks --site=$(SITE) --browser=chrome --headless -m "not playwright" -s -q

selenium-geolocation-parks-headed: ## Run Selenium nearby-park navigation test (headed Chrome)
	$(PYTEST) tests/internet/test_geolocation.py::test_geolocation_navigates_google_maps_top_10_named_parks --site=$(SITE) --browser=chrome -m "not playwright" -s -q

playwright-geolocation: ## Run Playwright geolocation tests (headless Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py -m playwright --pw-browser=chromium

playwright-geolocation-headed: ## Run Playwright geolocation tests (headed Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py -m playwright --pw-headed --pw-browser=chromium

playwright-geolocation-parks: ## Run Playwright nearby-park navigation test (headless Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py::test_geolocation_navigates_google_maps_all_nearby_parks_playwright -m playwright --pw-browser=chromium --pw-nav-wait-ms=$(NAV_WAIT_MS) -s -q

playwright-geolocation-parks-headed: ## Run Playwright nearby-park navigation test (headed Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py::test_geolocation_navigates_google_maps_all_nearby_parks_playwright -m playwright --pw-headed --pw-browser=chromium --pw-nav-wait-ms=$(NAV_WAIT_MS) -s -q

playwright-geolocation-parks-multistop: ## Run Playwright top named parks as one multi-stop route (headless Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py::test_geolocation_navigates_multi_stop_top_named_parks_playwright -m playwright --pw-browser=chromium --pw-nav-wait-ms=$(NAV_WAIT_MS) -s -q

playwright-geolocation-parks-multistop-headed: ## Run Playwright top named parks as one multi-stop route (headed Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py::test_geolocation_navigates_multi_stop_top_named_parks_playwright -m playwright --pw-headed --pw-browser=chromium --pw-nav-wait-ms=$(NAV_WAIT_MS) -s -q

playwright-geolocation-target: ## Run Playwright Target primary/backup routing test (headless Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py::test_geolocation_navigates_to_closest_target_with_backup_playwright -m playwright --pw-browser=chromium --pw-nav-wait-ms=$(NAV_WAIT_MS) -s -q

playwright-geolocation-target-headed: ## Run Playwright Target primary/backup routing test (headed Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py::test_geolocation_navigates_to_closest_target_with_backup_playwright -m playwright --pw-headed --pw-browser=chromium --pw-nav-wait-ms=$(NAV_WAIT_MS) -s -q

playwright-geolocation-target-park: ## Run Playwright nearest Target then Park route test (headless Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py::test_geolocation_navigates_to_nearest_target_then_park_playwright -m playwright --pw-browser=chromium --pw-nav-wait-ms=$(NAV_WAIT_MS) -s -q

playwright-geolocation-target-park-headed: ## Run Playwright nearest Target then Park route test (headed Chromium)
	$(PYTEST) tests/playwright/test_geolocation_pw.py::test_geolocation_navigates_to_nearest_target_then_park_playwright -m playwright --pw-headed --pw-browser=chromium --pw-nav-wait-ms=$(NAV_WAIT_MS) -s -q

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
