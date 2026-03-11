from __future__ import annotations

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright


def pytest_addoption(parser):
    parser.addoption(
        "--pw-browser",
        action="store",
        default="chromium",
        help="Playwright browser engine: chromium, firefox, webkit",
    )
    parser.addoption(
        "--pw-headed",
        action="store_true",
        help="Run Playwright in headed mode (default is headless)",
    )


@pytest.fixture(scope="session")
def pw_browser(request) -> Browser:
    engine = request.config.getoption("--pw-browser").lower()
    headed = request.config.getoption("--pw-headed")

    with sync_playwright() as p:
        browser_type = {
            "chromium": p.chromium,
            "firefox": p.firefox,
            "webkit": p.webkit,
        }.get(engine)

        if browser_type is None:
            raise pytest.UsageError(
                "Unknown --pw-browser value. Use one of: chromium, firefox, webkit"
            )

        browser = browser_type.launch(headless=not headed)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def pw_context(pw_browser: Browser) -> BrowserContext:
    context = pw_browser.new_context(ignore_https_errors=True)
    try:
        yield context
    finally:
        context.close()


@pytest.fixture
def pw_page(pw_context: BrowserContext) -> Page:
    page = pw_context.new_page()
    yield page


@pytest.fixture
def pw_page_object_factory(pw_page: Page, base_url: str):
    def _make(PageClass, *args, **kwargs):
        kwargs.setdefault("base_url", base_url)
        return PageClass(pw_page, *args, **kwargs)

    return _make
