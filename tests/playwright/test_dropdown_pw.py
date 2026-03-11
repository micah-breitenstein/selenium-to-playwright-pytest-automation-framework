from __future__ import annotations

import pytest

from pages.internet import PWDropdownPage


@pytest.mark.playwright
def test_dropdown_can_select_option_1_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDropdownPage)
    page.open()

    page.select_by_value("1")
    assert page.selected_text() == "Option 1"
