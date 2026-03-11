from __future__ import annotations

import pytest

from pages.internet import PWSortableTablesPage


@pytest.mark.playwright
def test_tables_have_four_rows_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWSortableTablesPage).load()
    assert page.row_count(1) == 4
