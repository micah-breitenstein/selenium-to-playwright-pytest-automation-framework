from __future__ import annotations

import pytest

from pages.internet import PWJavaScriptErrorPage


@pytest.mark.playwright
def test_javascript_error_page_loads_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJavaScriptErrorPage).load()
    assert page.body_text() is not None


@pytest.mark.playwright
def test_javascript_error_page_has_js_error_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJavaScriptErrorPage)

    errors: list[str] = []
    page.page.on("pageerror", lambda error: errors.append(str(error)))
    page.load()

    assert errors, "Expected a JavaScript error event"
    assert any("undefined" in msg.lower() or "error" in msg.lower() for msg in errors)
