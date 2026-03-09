# Selenium Pytest Page Object Cross Browser SauceLabs

![Python](https://img.shields.io/badge/python-3.14+-blue)
![Selenium](https://img.shields.io/badge/selenium-automation-green)
![pytest](https://img.shields.io/badge/pytest-testing-orange)

End-to-end UI test suite for [the-internet.herokuapp.com](https://the-internet.herokuapp.com) built with **Selenium 4**, **pytest**, and the **Page Object Model** pattern. Supports Chrome (local), Safari (local), and remote execution on **Sauce Labs**.

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

### Local – Safari (default browser)

```bash
python -m pytest --base-url=https://the-internet.herokuapp.com
```

### Local – Chrome

```bash
python -m pytest --browser=chrome --base-url=https://the-internet.herokuapp.com
```

### Local – Chrome headless + parallel

```bash
python -m pytest -n auto --browser=chrome --headless --base-url=https://the-internet.herokuapp.com
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
  --sauce-region=us-west-1 \
  --base-url=https://the-internet.herokuapp.com
```

### Remote – Sauce Labs (Chrome on macOS 13)

```bash
python -m pytest \
  --remote \
  --browser=chrome \
  --platform="macOS 13" \
  --browser-version=latest \
  --sauce-region=us-west-1 \
  --base-url=https://the-internet.herokuapp.com
```

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--browser` | `safari` | Browser to use: `safari`, `chrome`, `edge` |
| `--headless` | off | Run Chrome in headless mode |
| `--base-url` | `https://the-internet.herokuapp.com` | Application base URL |
| `--remote` | off | Run on Sauce Labs instead of locally |
| `--platform` | `Windows 11` | Sauce Labs OS platform |
| `--browser-version` | `latest` | Sauce Labs browser version |
| `--sauce-region` | `us-west-1` | Sauce Labs data center region |

## Project Structure

```
├── conftest.py              # Fixtures, CLI options, driver management
├── pytest.ini               # pytest settings and markers
├── requirements.txt         # Python dependencies
├── pages/
│   ├── __init__.py          # Lazy-loading page object registry
│   ├── core/
│   │   └── base_page.py     # BasePage – shared wait/click/type helpers
│   ├── components/
│   │   └── flash.py         # Reusable flash-message component
│   ├── landing_page.py      # Hub page for navigation
│   ├── login_page.py        # Login page object
│   └── ...                  # One page object per feature
├── tests/
│   ├── test_login_flow.py
│   ├── test_checkboxes.py
│   └── ...                  # One test module per feature
├── test_file/               # Static assets for upload tests
└── .github/
    └── workflows/
        └── ci.yml           # GitHub Actions – Chrome headless CI
```

## Architecture

- **BasePage** ([pages/core/base_page.py](pages/core/base_page.py)) provides `go()`, `click()`, `type()`, `wait_visible()`, `wait_clickable()`, and other helpers that all page objects inherit.
- **Lazy imports** via `pages/__init__.py` — page classes are only loaded when first accessed.
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
