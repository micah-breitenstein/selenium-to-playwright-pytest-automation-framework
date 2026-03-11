from __future__ import annotations

import pytest

from pages.internet import PWStatusCodesPage


@pytest.mark.playwright
def test_status_codes_return_link_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWStatusCodesPage).load()
    page.click_code(200)
    page.click_here_to_return()

    assert page.heading_text() == "Status Codes"
    assert page.current_url.endswith("/status_codes")
