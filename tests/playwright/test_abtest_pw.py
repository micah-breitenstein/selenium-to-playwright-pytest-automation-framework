from __future__ import annotations

import pytest

from pages.internet import PWABTestPage


@pytest.mark.playwright
def test_abtest_header_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWABTestPage)
    page.open()
    page.assert_header_is_valid()
