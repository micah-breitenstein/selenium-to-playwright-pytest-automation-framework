from __future__ import annotations

import pytest

from pages.internet import PWDynamicContentPage


@pytest.mark.playwright
def test_dynamic_content_has_rows_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDynamicContentPage).open_page()

    assert page.row_count() >= 3, f"Expected at least 3 rows, got {page.row_count()}"

    texts = page.rows_text()
    assert all(t.strip() for t in texts), (
        f"Expected non-empty text in all rows, got: {texts}"
    )
