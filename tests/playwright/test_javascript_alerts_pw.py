from __future__ import annotations

import pytest

from pages.internet import PWJavaScriptAlertsPage


@pytest.mark.playwright
def test_js_alert_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJavaScriptAlertsPage).open()

    page.accept_next_dialog().click_js_alert()

    assert page.result_text() == "You successfully clicked an alert"


@pytest.mark.playwright
def test_js_confirm_ok_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJavaScriptAlertsPage).open()

    page.accept_next_dialog().click_js_confirm()

    assert page.result_text() == "You clicked: Ok"


@pytest.mark.playwright
def test_js_confirm_cancel_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJavaScriptAlertsPage).open()

    page.dismiss_next_dialog().click_js_confirm()

    assert page.result_text() == "You clicked: Cancel"


@pytest.mark.playwright
def test_js_prompt_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJavaScriptAlertsPage).open()

    page.accept_next_dialog(prompt_text="Micah").click_js_prompt()

    assert page.result_text() == "You entered: Micah"
