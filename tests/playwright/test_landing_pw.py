from __future__ import annotations

import pytest

from pages.internet import PWLandingPage


@pytest.mark.playwright
def test_landing_navigation_to_login_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWLandingPage).load()
    page.go_to_login()

    assert page.current_url.endswith("/login")


@pytest.mark.playwright
def test_landing_navigation_to_dynamic_controls_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWLandingPage).load()
    page.go_to_dynamic_controls()

    assert page.current_url.endswith("/dynamic_controls")
