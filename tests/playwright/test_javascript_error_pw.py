from __future__ import annotations

import pytest

from pages.internet import PWJavaScriptErrorPage


@pytest.mark.playwright
def test_javascript_error_page_loads_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJavaScriptErrorPage).load()
    assert page.body_text() is not None
