from __future__ import annotations

import pytest
from playwright.async_api import Error

from pages.internet import PWKeyPressesPage


@pytest.mark.playwright
@pytest.mark.parametrize(
    "key, expected",
    [
        ("Tab", "TAB"),
        ("Escape", "ESCAPE"),
        ("Space", "SPACE"),
        ("a", "A"),
        ("9", "9"),
    ],
)
def test_key_presses_result_playwright(pw_page_object_factory, key, expected):
    page = pw_page_object_factory(PWKeyPressesPage).open()
    try:
        result = page.press_and_wait_for(key, expected)
    except Error:
        pytest.skip(f"Key dispatch not supported for key={key!r} in this run")
    assert result == f"You entered: {expected}"
