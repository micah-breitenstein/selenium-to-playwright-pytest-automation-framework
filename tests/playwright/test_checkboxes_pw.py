from __future__ import annotations

import pytest

from pages.internet import PWCheckboxesPage


@pytest.mark.playwright
def test_checkboxes_toggle_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWCheckboxesPage)
    page.open()

    assert page.is_checked(page.CB1) is False
    assert page.is_checked(page.CB2) is True

    page.set_checked(page.CB1, True)
    page.set_checked(page.CB2, False)

    assert page.is_checked(page.CB1) is True
    assert page.is_checked(page.CB2) is False
