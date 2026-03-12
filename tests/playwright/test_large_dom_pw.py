from __future__ import annotations

import re

import pytest

from pages.internet import PWLargeDomPage


@pytest.mark.playwright
def test_large_dom_table_dimensions_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWLargeDomPage).load()

    rows = page.row_count()
    cols = page.column_count()

    assert rows >= 50, f"Expected at least 50 rows, got {rows}"
    assert cols >= 50, f"Expected at least 50 columns, got {cols}"


@pytest.mark.playwright
def test_large_dom_cell_text_format_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWLargeDomPage).load()

    cells = [
        page.page.locator("#large-table tbody tr")
        .nth(0)
        .locator("td")
        .nth(0)
        .inner_text(),
        page.page.locator("#large-table tbody tr")
        .nth(24)
        .locator("td")
        .nth(24)
        .inner_text(),
        page.page.locator("#large-table tbody tr")
        .nth(49)
        .locator("td")
        .nth(49)
        .inner_text(),
    ]

    for text in cells:
        assert re.fullmatch(r"\d+\.\d+", text.strip()), (
            f"Unexpected cell text: {text!r}"
        )
