from __future__ import annotations

import pytest

from pages.internet import PWDragAndDropPage


@pytest.mark.playwright
def test_drag_and_drop_swaps_twice_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDragAndDropPage).open()

    before = page.header_texts()
    assert before == ("A", "B")

    page.swap_columns_html5()
    assert page.header_texts() == ("B", "A")

    page.swap_columns_html5()
    assert page.header_texts() == ("A", "B")
