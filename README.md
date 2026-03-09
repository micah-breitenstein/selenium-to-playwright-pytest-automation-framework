# Selenium Pytest Page Object Cross Browser SauceLabs

![Python](https://img.shields.io/badge/python-3.14+-blue)
![Selenium](https://img.shields.io/badge/selenium-automation-green)
![pytest](https://img.shields.io/badge/pytest-testing-orange)

End-to-end UI test suite built with **Selenium 4**, **pytest**, and the **Page Object Model** pattern. Supports multiple target websites, Chrome (local), Safari (local), and remote execution on **Sauce Labs**.

---

## Prerequisites

- Python 3.14+
- Google Chrome (local) and/or Safari (local)
- [Sauce Labs](https://saucelabs.com) account (for remote execution)

## Quick Start

```bash
git clone git@github.com:micah-breitenstein/selenium-pytest-pageobject-cross-browser-saucelabs.git
cd selenium-pytest-pageobject-cross-browser-saucelabs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running Tests

The `--site` flag selects a target website from the built-in registry (`config/sites.py`). When omitted it defaults to `internet` (the-internet.herokuapp.com).

### Local – Safari (default browser, default site)

```bash
python -m pytest
```

### Local – Chrome

```bash
python -m pytest --browser=chrome
```

### Local – Chrome headless + parallel

```bash
python -m pytest -n auto --browser=chrome --headless
```

### Specify a site explicitly

```bash
python -m pytest --site=internet            # the-internet.herokuapp.com
python -m pytest --site=saucedemo           # saucedemo.com
python -m pytest --site=demoqa              # demoqa.com
```

### Override the base URL directly

`--base-url` takes precedence over `--site` when both are provided:

```bash
python -m pytest --base-url=http://localhost:8080
```

### Remote – Sauce Labs (Edge on Windows 11)

```bash
export SAUCE_USERNAME=<your-username>
export SAUCE_ACCESS_KEY=<your-access-key>

python -m pytest \
  --remote \
  --browser=edge \
  --platform="Windows 11" \
  --browser-version=latest \
  --sauce-region=us-west-1
```

### Remote – Sauce Labs (Chrome on macOS 13)

```bash
python -m pytest \
  --remote \
  --browser=chrome \
  --platform="macOS 13" \
  --browser-version=latest \
  --sauce-region=us-west-1
```

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--site` | `internet` | Target site alias (see `config/sites.py`) |
| `--browser` | `safari` | Browser to use: `safari`, `chrome`, `edge` |
| `--headless` | off | Run Chrome in headless mode |
| `--base-url` | *(from site)* | Explicit base URL (overrides `--site`) |
| `--remote` | off | Run on Sauce Labs instead of locally |
| `--platform` | `Windows 11` | Sauce Labs OS platform |
| `--browser-version` | `latest` | Sauce Labs browser version |
| `--sauce-region` | `us-west-1` | Sauce Labs data center region |

### Registered Sites

| Alias | URL |
|-------|-----|
| `internet` | `https://the-internet.herokuapp.com` |
| `saucedemo` | `https://www.saucedemo.com` |
| `demoqa` | `https://demoqa.com` |

To add a new site, add an entry to `config/sites.py` and create matching `pages/<alias>/` and `tests/<alias>/` packages.

## Project Structure

```
├── conftest.py              # Fixtures, CLI options, driver management
├── pytest.ini               # pytest settings and markers
├── requirements.txt         # Python dependencies
├── config/
│   └── sites.py             # SITES registry (alias → URL)
├── pages/
│   ├── __init__.py          # Backward-compatible re-exports (delegates to internet)
│   ├── core/
│   │   └── base_page.py     # BasePage – shared wait/click/type helpers
│   ├── components/
│   │   └── flash.py         # Reusable flash-message component
│   ├── internet/            # Page objects for the-internet.herokuapp.com
│   │   ├── __init__.py      # Lazy-loading registry for this site
│   │   ├── landing_page.py
│   │   ├── login_page.py
│   │   └── ...              # One page object per feature
│   ├── saucedemo/           # (placeholder) Page objects for saucedemo.com
│   └── demoqa/              # (placeholder) Page objects for demoqa.com
├── tests/
│   ├── internet/            # Tests for the-internet.herokuapp.com
│   │   ├── test_login_flow.py
│   │   ├── test_checkboxes.py
│   │   └── ...
│   ├── saucedemo/           # (placeholder) Tests for saucedemo.com
│   └── demoqa/              # (placeholder) Tests for demoqa.com
├── test_file/               # Static assets for upload tests
└── .github/
    └── workflows/
        └── ci.yml           # GitHub Actions – Chrome headless CI
```

## Architecture

- **BasePage** ([pages/core/base_page.py](pages/core/base_page.py)) provides `go()`, `click()`, `type()`, `wait_visible()`, `wait_clickable()`, and other helpers that all page objects inherit.
- **Multi-site layout** — pages and tests are organized by site under `pages/<alias>/` and `tests/<alias>/`. The top-level `pages/__init__.py` delegates to `pages.internet` so existing `from pages import X` imports continue to work.
- **Lazy imports** via each site's `__init__.py` — page classes are only loaded when first accessed.
- **Driver scoping** — Chrome/remote drivers are module-scoped for speed; Safari is function-scoped for stability.
- **Retry logic** — Remote session creation retries on Sauce Labs concurrent-session-limit errors.

## Markers

| Marker | Purpose |
|--------|---------|
| `@pytest.mark.no_safari` | Skip test when running under Safari (e.g. CDP-only features) |

## Failure Artifacts

When tests fail the framework automatically captures:

- Browser screenshots
- Logs
- Test metadata

Artifacts are stored in the `artifacts/` directory.
