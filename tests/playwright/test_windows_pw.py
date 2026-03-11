from __future__ import annotations

import pytest

from pages.internet import PWWindowsPage


@pytest.mark.playwright
def test_windows_opens_new_window_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWWindowsPage).load()

    page.open_new_window()
    assert page.heading_text() == "New Window"

    page.close_current_window()
    page.switch_to_first_window()
    assert page.heading_text() == "Opening a new window"
