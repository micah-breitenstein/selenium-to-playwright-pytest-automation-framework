import re

import pytest

from pages import SortableTablesPage

SORTABLE_COLUMNS = ["Last Name", "First Name", "Email", "Due", "Web Site"]


def _sort_key(column: str):
    """Return a sort-key function appropriate for the column type."""
    if column == "Due":
        # Currency values like "$50.00" — sort numerically
        return lambda v: float(re.sub(r"[^\d.]", "", v))
    return str.casefold


def test_tables_page_heading(driver, base_url):
    page = SortableTablesPage(driver, base_url=base_url).load()

    assert page.heading_text() == "Data Tables"


@pytest.mark.parametrize("table_id", [1, 2])
def test_tables_have_four_rows(driver, base_url, table_id):
    page = SortableTablesPage(driver, base_url=base_url).load()

    assert page.row_count(table_id) == 4


@pytest.mark.parametrize("table_id", [1, 2])
def test_tables_have_correct_headers(driver, base_url, table_id):
    page = SortableTablesPage(driver, base_url=base_url).load()

    headers = page.header_texts(table_id)
    assert headers == ["Last Name", "First Name", "Email", "Due", "Web Site", "Action"]


@pytest.mark.parametrize("table_id", [1, 2])
@pytest.mark.parametrize("column", SORTABLE_COLUMNS)
def test_sort_ascending(driver, base_url, table_id, column):
    page = SortableTablesPage(driver, base_url=base_url).load()

    values = page.sort_ascending(column, table_id)
    key = _sort_key(column)
    assert values == sorted(values, key=key), (
        f"Table {table_id}, column '{column}' not sorted ascending: {values}"
    )


@pytest.mark.parametrize("table_id", [1, 2])
@pytest.mark.parametrize("column", SORTABLE_COLUMNS)
def test_sort_descending(driver, base_url, table_id, column):
    page = SortableTablesPage(driver, base_url=base_url).load()

    values = page.sort_descending(column, table_id)
    key = _sort_key(column)
    assert values == sorted(values, key=key, reverse=True), (
        f"Table {table_id}, column '{column}' not sorted descending: {values}"
    )


# ---- Action link tests ----


@pytest.mark.parametrize("table_id", [1, 2])
def test_edit_link_updates_url(driver, base_url, table_id):
    page = SortableTablesPage(driver, base_url=base_url).load()

    url = page.click_edit(row=0, table_id=table_id)
    assert url.endswith("#edit")


@pytest.mark.parametrize("table_id", [1, 2])
def test_delete_link_updates_url(driver, base_url, table_id):
    page = SortableTablesPage(driver, base_url=base_url).load()

    url = page.click_delete(row=0, table_id=table_id)
    assert url.endswith("#delete")
