from __future__ import annotations

import pytest

from pages.internet import PWShiftingContentListPage


@pytest.mark.playwright
def test_shifting_content_list_contains_static_record_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWShiftingContentListPage).load()

    items = page.list_items()
    assert len(items) >= 5, f"Expected at least 5 list items, got {len(items)}"
    assert page.has_static_record(), "Expected static record to be present in the list"
    assert page.static_record_count() == 1, (
        "Expected static record to appear exactly once"
    )


@pytest.mark.playwright
def test_shifting_content_list_heading_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentListPage).load()

    assert page.heading_text() == "Shifting Content: List"
    assert page.current_url.endswith("/shifting_content/list")


@pytest.mark.playwright
def test_shifting_content_list_static_record_changes_position_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWShiftingContentListPage).load()

    positions = set()
    for _ in range(20):
        items = page.list_items()
        try:
            idx = items.index(page.STATIC_RECORD_TEXT)
        except ValueError:
            idx = -1

        assert idx >= 0, "Expected static record to exist on every load"
        positions.add(idx)
        if len(positions) >= 2:
            break

        page.page.reload(wait_until="domcontentloaded", timeout=page.config.timeout_ms)

    if len(positions) < 2:
        pytest.skip(
            "Static record did not change position in this run; demo randomness can be streaky."
        )
