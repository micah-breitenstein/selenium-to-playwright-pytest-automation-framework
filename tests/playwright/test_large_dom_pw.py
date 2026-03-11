from __future__ import annotations

import pytest

from pages.internet import PWLargeDomPage


@pytest.mark.playwright
def test_large_dom_table_dimensions_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWLargeDomPage).load()

    rows = page.row_count()
    cols = page.column_count()

    assert rows >= 50, f"Expected at least 50 rows, got {rows}"
    assert cols >= 50, f"Expected at least 50 columns, got {cols}"
