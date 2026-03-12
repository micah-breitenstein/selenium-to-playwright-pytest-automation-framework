from __future__ import annotations

import re

import pytest

from pages.internet import PWSortableTablesPage

SORTABLE_COLUMNS = ["Last Name", "First Name", "Email", "Due", "Web Site"]


def _sort_key(column: str):
    if column == "Due":
        return lambda v: float(re.sub(r"[^\d.]", "", v))
    return str.casefold


def _column_index(column: str) -> int:
    return {
        "Last Name": 0,
        "First Name": 1,
        "Email": 2,
        "Due": 3,
        "Web Site": 4,
        "Action": 5,
    }[column]


def _table_base(table_id: int) -> str:
    return f"#table{table_id}"


def _header_texts(page: PWSortableTablesPage, table_id: int) -> list[str]:
    base = _table_base(table_id)
    return [
        text.strip()
        for text in page.page.locator(f"{base} thead th span").all_inner_texts()
    ]


def _column_values(page: PWSortableTablesPage, column: str, table_id: int) -> list[str]:
    base = _table_base(table_id)
    col_idx = _column_index(column)
    rows = page.page.locator(f"{base} tbody tr")
    values = []
    for i in range(rows.count()):
        values.append(rows.nth(i).locator("td").nth(col_idx).inner_text().strip())
    return values


def _click_sort(page: PWSortableTablesPage, column: str, table_id: int) -> None:
    base = _table_base(table_id)
    col_idx = _column_index(column)
    page.page.locator(f"{base} thead th span").nth(col_idx).click(
        timeout=page.config.timeout_ms
    )
    page.page.wait_for_timeout(300)


@pytest.mark.playwright
@pytest.mark.parametrize("table_id", [1, 2])
def test_tables_have_four_rows_playwright(pw_page_object_factory, table_id):
    page = pw_page_object_factory(PWSortableTablesPage).load()
    assert page.row_count(table_id) == 4


@pytest.mark.playwright
def test_tables_page_heading_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWSortableTablesPage).load()
    assert page.heading_text() == "Data Tables"


@pytest.mark.playwright
@pytest.mark.parametrize("table_id", [1, 2])
def test_tables_have_correct_headers_playwright(pw_page_object_factory, table_id):
    page = pw_page_object_factory(PWSortableTablesPage).load()
    headers = _header_texts(page, table_id)
    assert headers == [
        "Last Name",
        "First Name",
        "Email",
        "Due",
        "Web Site",
        "Action",
    ]


@pytest.mark.playwright
@pytest.mark.parametrize("table_id", [1, 2])
@pytest.mark.parametrize("column", SORTABLE_COLUMNS)
def test_sort_ascending_playwright(pw_page_object_factory, table_id, column):
    page = pw_page_object_factory(PWSortableTablesPage).load()

    _click_sort(page, column, table_id)
    values = _column_values(page, column, table_id)
    key = _sort_key(column)
    assert values == sorted(values, key=key), (
        f"Table {table_id}, column '{column}' not sorted ascending: {values}"
    )


@pytest.mark.playwright
@pytest.mark.parametrize("table_id", [1, 2])
@pytest.mark.parametrize("column", SORTABLE_COLUMNS)
def test_sort_descending_playwright(pw_page_object_factory, table_id, column):
    page = pw_page_object_factory(PWSortableTablesPage).load()

    _click_sort(page, column, table_id)
    _click_sort(page, column, table_id)
    values = _column_values(page, column, table_id)
    key = _sort_key(column)
    assert values == sorted(values, key=key, reverse=True), (
        f"Table {table_id}, column '{column}' not sorted descending: {values}"
    )


@pytest.mark.playwright
@pytest.mark.parametrize("table_id", [1, 2])
def test_edit_link_updates_url_playwright(pw_page_object_factory, table_id):
    page = pw_page_object_factory(PWSortableTablesPage).load()
    base = _table_base(table_id)

    page.page.locator(f"{base} tbody tr").nth(0).locator("a", has_text="edit").click(
        timeout=page.config.timeout_ms
    )
    assert page.current_url.endswith("#edit")


@pytest.mark.playwright
@pytest.mark.parametrize("table_id", [1, 2])
def test_delete_link_updates_url_playwright(pw_page_object_factory, table_id):
    page = pw_page_object_factory(PWSortableTablesPage).load()
    base = _table_base(table_id)

    page.page.locator(f"{base} tbody tr").nth(0).locator("a", has_text="delete").click(
        timeout=page.config.timeout_ms
    )
    assert page.current_url.endswith("#delete")
