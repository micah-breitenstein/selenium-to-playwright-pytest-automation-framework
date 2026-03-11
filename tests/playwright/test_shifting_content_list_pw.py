from __future__ import annotations

import pytest

from pages.internet import PWShiftingContentListPage


@pytest.mark.playwright
def test_shifting_content_list_contains_static_record_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentListPage).load()

    items = page.list_items()
    assert len(items) >= 5, f"Expected at least 5 list items, got {len(items)}"
    assert page.has_static_record(), "Expected static record to be present in the list"
    assert page.static_record_count() == 1, "Expected static record to appear exactly once"
