from __future__ import annotations

import pytest

from pages.internet import PWAddRemoveElementsPage


@pytest.mark.playwright
def test_add_one_delete_button_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWAddRemoveElementsPage)
    page.open()

    page.add_element()
    page.wait_for_delete_count(1)
    assert page.delete_count() == 1
