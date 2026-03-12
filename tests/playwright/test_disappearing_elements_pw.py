from __future__ import annotations

import pytest

from pages.internet import PWDisappearingElementsPage


@pytest.mark.playwright
def test_core_menu_items_are_present_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDisappearingElementsPage).open()

    texts = page.menu_texts()

    for required in ["Home", "About", "Contact Us", "Portfolio"]:
        assert required in texts, f"Expected '{required}' in menu, got {texts}"


@pytest.mark.playwright
def test_gallery_menu_item_is_optional_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDisappearingElementsPage).open()
    _ = page.has_menu_item("Gallery")


@pytest.mark.playwright
def test_gallery_eventually_appears_demo_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDisappearingElementsPage).open()

    for _ in range(10):
        if page.has_menu_item("Gallery"):
            return
        page.refresh()

    assert False, "Gallery did not appear after 10 refreshes (random behavior)"
