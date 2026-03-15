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
    parser.addoption(
        "--pw-slowmo",
        action="store",
        type=int,
        default=0,
        metavar="MS",
        help="Slow down Playwright operations by MS milliseconds (useful with --pw-headed)",
    )
    parser.addoption(
        "--pw-nav-wait-ms",
        action="store",
        type=int,
        default=0,
        metavar="MS",
        help="Wait MS after each Google Maps navigation in park-route tests (default: 0)",
    )


@pytest.fixture(scope="session")
def pw_browser(request) -> Browser:
    engine = str(request.config.getoption("--pw-browser", default="chromium")).lower()
    headed = bool(request.config.getoption("--pw-headed", default=False))
    slowmo = int(request.config.getoption("--pw-slowmo", default=0))

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

        browser = browser_type.launch(headless=not headed, slow_mo=slowmo)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def pw_context(pw_browser: Browser, base_url: str) -> BrowserContext:
    context = pw_browser.new_context(ignore_https_errors=True)
    context.grant_permissions(["geolocation"], origin=base_url)
    try:
        yield context
    finally:
        context.close()


@pytest.fixture
def pw_page(pw_context: BrowserContext) -> Page:
    page = pw_context.new_page()
    yield page


@pytest.fixture
def pw_nav_wait_ms(request) -> int:
    return int(request.config.getoption("--pw-nav-wait-ms", default=0))


@pytest.fixture
def pw_page_object_factory(pw_page: Page, base_url: str):
    def _make(PageClass, *args, **kwargs):
        kwargs.setdefault("base_url", base_url)
        return PageClass(pw_page, *args, **kwargs)

    return _make


@pytest.fixture
def pw_mock_geolocation(pw_context: BrowserContext, base_url: str):
    """Configure mocked geolocation for Playwright tests."""

    def _set(latitude: float, longitude: float, accuracy: int = 10):
        pw_context.set_geolocation(
            {
                "latitude": latitude,
                "longitude": longitude,
                "accuracy": accuracy,
            }
        )

    return _set
