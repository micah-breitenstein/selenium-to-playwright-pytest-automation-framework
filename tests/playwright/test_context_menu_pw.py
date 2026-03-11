from __future__ import annotations

import pytest

from pages.internet import PWContextMenuPage


@pytest.mark.playwright
def test_context_menu_alert_can_be_accepted_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWContextMenuPage).open()
    message = page.context_click_hotspot_and_accept_alert()
    assert message == "You selected a context menu"
