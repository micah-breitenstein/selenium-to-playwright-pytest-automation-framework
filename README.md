# Selenium Pytest Page Object Cross Browser SauceLabs

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Selenium](https://img.shields.io/badge/selenium-automation-green)
![pytest](https://img.shields.io/badge/pytest-testing-orange)

End-to-end UI automation framework built with **Python, Selenium WebDriver, and pytest**.

The framework demonstrates scalable automation practices including:

- Page Object Model (POM)
- Cross-browser testing (Safari, Chrome, Firefox, Edge)
- Local and Sauce Labs cloud execution
- Pytest fixtures and CLI configuration
- Screenshot capture on failure
- Parallel test execution
- Structured page objects and reusable components

---

# Application Under Test

Tests target the public Selenium practice site:

https://the-internet.herokuapp.com

The suite includes coverage for:

- Authentication
- File uploads and downloads
- Dynamic elements
- Floating menus
- Large DOM tables
- iFrame interactions
- jQuery UI components

---

# Framework Architecture

The project follows the **Page Object Model (POM)** design pattern to promote maintainability, readability, and reuse.

```
project-root
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── file_upload_page.py
│   └── ...
│
├── tests/
│   ├── test_login.py
│   ├── test_file_upload.py
│   └── ...
│
├── artifacts/
│   └── screenshots and logs
│
├── conftest.py
└── pytest.ini
```

### Key Components

**Page Objects**

- Encapsulate page locators and UI behavior
- Provide reusable interactions for tests
- Reduce duplication in test logic

**Tests**

- Contain assertions and user workflows
- Use page objects to keep tests readable

**Fixtures**

Defined in `conftest.py` to manage:

- browser initialization
- CLI configuration
- remote execution with Sauce Labs

---

# Technologies Used

- Python
- Selenium WebDriver
- pytest
- pytest-xdist (parallel testing)
- webdriver-manager
- Sauce Labs

---

# Installation

Clone the repository and install dependencies.

```bash
git clone git@github.com:micah-breitenstein/selenium-pytest-pageobject-cross-browser-saucelabs.git
cd selenium-pytest-pageobject-cross-browser-saucelabs

python3 -m venv .venv
source .venv/bin/activate

pip install pytest selenium webdriver-manager pytest-xdist
```

---

# Running Tests

## Run Locally

Default browser (Safari)

```bash
pytest -q
```

Chrome

```bash
pytest -q --browser=chrome
```

Chrome headless

```bash
pytest -q --browser=chrome --headless
```

---

# Run Tests in Parallel

Parallel execution uses **pytest-xdist**.

```bash
pytest -n auto -q --browser=chrome
```

This automatically distributes tests across available CPU cores.

---

# Test a Local Application (127.0.0.1)

Safari

```bash
python -m pytest -q -s --base-url=http://127.0.0.1:9292
```

Chrome

```bash
python -m pytest -q -s --browser=chrome --base-url=http://127.0.0.1:9292
```

Chrome headless

```bash
python -m pytest -q -s --browser=chrome --headless --base-url=http://127.0.0.1:9292
```

---

# Test the Public Demo Site

```bash
python -m pytest -q -s --base-url=https://the-internet.herokuapp.com
```

Chrome

```bash
python -m pytest -q -s --browser=chrome --base-url=https://the-internet.herokuapp.com
```

Headless

```bash
python -m pytest -q --browser=chrome --headless --base-url=https://the-internet.herokuapp.com
```

---

# Sauce Labs Setup

Set your Sauce Labs credentials as environment variables.

```bash
export SAUCE_USERNAME=your_username
export SAUCE_ACCESS_KEY=your_access_key
```

---

# Running Tests on Sauce Labs

## Edge on Windows 11

```bash
python -m pytest -q \
  --remote \
  --browser=edge \
  --platform="Windows 11" \
  --browser-version=latest \
  --sauce-region=us-west-1 \
  --base-url=https://the-internet.herokuapp.com
```

## Chrome on macOS 13

```bash
python -m pytest -q \
  --remote \
  --browser=chrome \
  --platform="macOS 13" \
  --browser-version=latest \
  --sauce-region=us-west-1 \
  --base-url=https://the-internet.herokuapp.com
```

---

# Failure Artifacts

When tests fail the framework automatically captures:

- browser screenshots
- logs
- test metadata

Artifacts are stored in the `artifacts/` directory.

---

# Key Automation Features Demonstrated

This project demonstrates real-world automation engineering techniques:

- Page Object Model test architecture
- Cross-browser testing
- Local and cloud execution
- Parallel testing with pytest-xdist
- Structured test organization
- Reusable page abstractions
