from __future__ import annotations

import pytest

from pages.internet import PWStatusCodesPage


@pytest.mark.playwright
@pytest.mark.parametrize("code", [200, 301, 404, 500])
def test_status_code_page_displays_message_playwright(pw_page_object_factory, code):
    page = pw_page_object_factory(PWStatusCodesPage).load()
    page.click_code(code)

    assert f"/status_codes/{code}" in page.current_url
    assert str(code) in page.result_text()


@pytest.mark.playwright
def test_status_codes_landing_heading_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWStatusCodesPage).load()
    assert page.heading_text() == "Status Codes"


@pytest.mark.playwright
def test_status_codes_return_link_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWStatusCodesPage).load()
    page.click_code(200)
    page.click_here_to_return()

    assert page.heading_text() == "Status Codes"
    assert page.current_url.endswith("/status_codes")
