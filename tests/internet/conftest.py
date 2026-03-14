# tests/internet/conftest.py
"""
Fixtures specific to the-internet.herokuapp.com test suite.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def internet_page(page):
    """
    Convenience wrapper around the generic ``page`` factory.

    Usage::

        def test_example(internet_page):
            login = internet_page(LoginPage)
            login.go("/login")
    """
    return page


@pytest.fixture
def navigate(landing):
    """
    Return the landing page already loaded and ready for navigation.

    Usage::

        def test_checkboxes(navigate):
            cb = navigate.go_to_checkboxes()
    """
    return landing.load()


@pytest.fixture
def mock_geolocation(driver, request, base_url):
    """
    Configure browser geolocation for Chrome/Edge Selenium sessions.

    Usage::

        def test_example(mock_geolocation):
            mock_geolocation(37.7749, -122.4194)
    """

    browser = request.config.getoption("--browser")
    if browser == "safari":
        pytest.skip("Geolocation override fixture is not supported on Safari")

    def _set(latitude: float, longitude: float, accuracy: int = 10):
        origin = base_url.rstrip("/")
        driver.execute_cdp_cmd(
            "Browser.grantPermissions",
            {
                "origin": origin,
                "permissions": ["geolocation"],
            },
        )
        driver.execute_cdp_cmd(
            "Emulation.setGeolocationOverride",
            {
                "latitude": latitude,
                "longitude": longitude,
                "accuracy": accuracy,
            },
        )

    return _set


@pytest.fixture
def deny_geolocation(driver, request, base_url):
    """
    Deny geolocation permission for Chrome/Edge Selenium sessions.
    """

    browser = request.config.getoption("--browser")
    if browser == "safari":
        pytest.skip("Geolocation deny fixture is not supported on Safari")

    origin = base_url.rstrip("/")
    driver.execute_cdp_cmd(
        "Browser.setPermission",
        {
            "origin": origin,
            "permission": {"name": "geolocation"},
            "setting": "denied",
        },
    )

    return True
