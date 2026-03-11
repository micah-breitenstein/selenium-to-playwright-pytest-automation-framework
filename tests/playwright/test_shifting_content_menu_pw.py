from __future__ import annotations

import pytest

from pages.internet import PWShiftingContentMenuPage

EXPECTED_MENU_ITEMS = ["Home", "About", "Contact Us", "Portfolio", "Gallery"]


@pytest.mark.playwright
def test_shifting_content_menu_items_default_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentMenuPage).load()

    assert page.menu_items() == EXPECTED_MENU_ITEMS
    assert page.current_url.endswith("/shifting_content/menu")
