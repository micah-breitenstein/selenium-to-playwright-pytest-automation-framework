from __future__ import annotations

import pytest

from pages.internet import PWFloatingMenuPage


@pytest.mark.playwright
def test_floating_menu_stays_visible_and_updates_hash_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWFloatingMenuPage).open()

    assert page.menu_is_displayed(), "Menu should be visible on load"

    page.scroll_to_bottom()
    assert page.menu_is_displayed(), "Menu should remain visible after scroll"

    page.click_menu_item("About")
    assert page.current_hash().lower() == "#about"
