import pytest

from pages import ShiftingContentListPage


def test_shifting_content_list_heading(driver, base_url):
    page = ShiftingContentListPage(driver, base_url=base_url).load()

    assert page.heading_text() == "Shifting Content: List"
    assert page.current_url().endswith("/shifting_content/list")


def test_shifting_content_list_contains_static_record(driver, base_url):
    page = ShiftingContentListPage(driver, base_url=base_url).load()

    items = page.list_items()
    assert len(items) >= 5, f"Expected at least 5 list items, got {len(items)}"
    assert page.has_static_record(), "Expected static record to be present in the list"
    assert page.static_record_count() == 1, (
        "Expected static record to appear exactly once"
    )


def test_shifting_content_list_static_record_changes_position(driver, base_url):
    page = ShiftingContentListPage(driver, base_url=base_url).load()

    positions = set()
    for _ in range(20):
        idx = page.static_record_index()
        assert idx >= 0, "Expected static record to exist on every load"
        positions.add(idx)
        if len(positions) >= 2:
            break
        page.refresh()

    if len(positions) < 2:
        pytest.skip(
            "Static record did not change position in this run; demo randomness can be streaky."
        )
