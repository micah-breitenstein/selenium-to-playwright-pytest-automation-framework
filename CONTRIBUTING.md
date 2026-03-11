# Contributing

Thanks for your interest in contributing!

## Setup

```bash
git clone git@github.com:micah-breitenstein/selenium-pytest-pageobject-cross-browser-saucelabs.git
cd selenium-pytest-pageobject-cross-browser-saucelabs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
```

Alternative shell activation commands:

```bash
# fish
source .venv/bin/activate.fish

# csh/tcsh
source .venv/bin/activate.csh
```

## Playwright (side-by-side with Selenium)

This repo now supports a minimal Playwright path in parallel with Selenium.

- Playwright base page: `pages/core/pw_base_page.py`
- Example Playwright page object: `pages/example/pw_homepage.py`
- Playwright fixtures/tests: `tests/playwright/`

Run only Playwright tests:

```bash
python -m pytest tests/playwright -m playwright
```

Switch Playwright engine:

```bash
python -m pytest tests/playwright -m playwright --pw-browser=webkit
python -m pytest tests/playwright -m playwright --pw-browser=firefox
```

Run headed mode:

```bash
python -m pytest tests/playwright -m playwright --pw-headed
```

Makefile shortcuts:

```bash
make pw-test
make pw-headed
make pw-parallel
```

Quick quality gate before opening a PR:

```bash
make check
```

Note on external TinyMCE AI docs tests:

- A subset of tests may be skipped when the third-party demo editor is non-interactive at runtime.
- This is expected behavior to avoid false negatives from external service instability.

## Adding a New Site

1. Add an entry to `config/sites.py`:

   ```python
   SITES["mysite"] = "https://example.com"
   ```

2. Create the page object and test packages:

   ```
   pages/mysite/__init__.py
   tests/mysite/__init__.py
   ```

3. Add page objects under `pages/mysite/` — each should inherit from `BasePage`:

   ```python
   from pages.core.base_page import BasePage

   class MyLoginPage(BasePage):
       ...
   ```

4. Add tests under `tests/mysite/`. Use the `page` fixture to instantiate page objects:

   ```python
   from pages.mysite.my_login_page import MyLoginPage

   def test_login(page):
       login = page(MyLoginPage)
       login.go("/login")
   ```

5. Run tests for the new site:

   ```bash
   python -m pytest --site=mysite --browser=chrome --headless
   ```

## Adding a Page Object (existing site)

1. Create `pages/<site>/my_page.py` with a class inheriting from `BasePage`.
2. Add the class to `pages/<site>/__init__.py` in the `_EXPORTS` dict.
3. Add a matching test file `tests/<site>/test_my_page.py`.

## Adding a Test

- Place test files under `tests/<site>/`.
- Use the `page` factory fixture or the `landing` fixture for the‑internet tests.
- Mark Safari-incompatible tests with `@pytest.mark.no_safari`.

## Running Tests

```bash
# Default site (internet), Safari
python -m pytest

# Chrome headless, parallel
python -m pytest -n auto --browser=chrome --headless

# Specific site
python -m pytest --site=saucedemo --browser=chrome --headless
```

## Linting

```bash
pip install ruff
ruff check .
ruff format --check .
```

## Code Style

- Use the **Page Object Model** — one class per page/feature.
- Inherit from `BasePage` for all page objects.
- Keep locators as class-level constants using `(By.*, "...")` tuples.
- Prefer `BasePage` helpers (`click`, `type`, `wait_visible`, etc.) over raw Selenium calls.
- Add type hints to method signatures.
