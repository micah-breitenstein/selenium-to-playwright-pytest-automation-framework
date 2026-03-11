from __future__ import annotations

import pytest

from pages.internet import PWDisappearingElementsPage


@pytest.mark.playwright
def test_core_menu_items_are_present_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDisappearingElementsPage).open()

    texts = page.menu_texts()

    for required in ["Home", "About", "Contact Us", "Portfolio"]:
        assert required in texts, f"Expected '{required}' in menu, got {texts}"
