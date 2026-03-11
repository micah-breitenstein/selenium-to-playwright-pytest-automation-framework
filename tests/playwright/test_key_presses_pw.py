from __future__ import annotations

import pytest

from pages.internet import PWKeyPressesPage


@pytest.mark.playwright
def test_key_presses_result_a_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWKeyPressesPage).open()
    result = page.press_and_wait_for("a", "A")
    assert result == "You entered: A"
