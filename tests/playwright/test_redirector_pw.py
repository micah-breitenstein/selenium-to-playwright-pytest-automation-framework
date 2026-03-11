from __future__ import annotations

import pytest

from pages.internet import PWRedirectorPage


@pytest.mark.playwright
def test_redirector_navigates_to_status_codes_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWRedirectorPage).load()

    assert page.heading_text() == "Redirection"

    page.click_redirect()
    page.wait_for_url_contains("/status_codes")

    assert "/status_codes" in page.current_url
