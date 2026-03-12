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


@pytest.mark.playwright
def test_dynamic_content_changes_after_refresh_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDynamicContentPage).open_page()

    before = page.rows_text()

    changed = False
    for _ in range(5):
        page.refresh()
        after = page.rows_text()
        if after != before:
            changed = True
            break

    assert changed


@pytest.mark.playwright
def test_dynamic_content_static_mode_most_text_stays_same_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWDynamicContentPage).open_page(static=True)

    before = page.rows_text()
    assert before, "Expected at least one non-empty text row"

    for _ in range(3):
        page.refresh()
        after = page.rows_text()

        pairs = list(zip(before, after))
        same_count = sum(1 for b, a in pairs if b == a)

        assert same_count >= 2, (
            f"Expected most static rows to stay same. same_count={same_count}"
            f"\nBefore={before}\nAfter={after}"
        )


@pytest.mark.playwright
def test_dynamic_content_dynamic_mode_text_changes_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDynamicContentPage).open_page(static=False)

    before = page.rows_text()
    assert before, "Expected at least one non-empty text row"

    changed = False
    last = before
    for _ in range(5):
        page.refresh()
        last = page.rows_text()
        if last != before:
            changed = True
            break

    assert changed, (
        f"Expected dynamic text to change within 5 refreshes. Before={before}, Last={last}"
    )
