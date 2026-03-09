import re

from pages import LargeDomPage


def test_large_dom_table_dimensions(driver, base_url):
    page = LargeDomPage(driver, base_url=base_url).load()

    rows = page.row_count()
    cols = page.column_count()

    assert rows >= 50, f"Expected at least 50 rows, got {rows}"
    assert cols >= 50, f"Expected at least 50 columns, got {cols}"


def test_large_dom_cell_text_format(driver, base_url):
    page = LargeDomPage(driver, base_url=base_url).load()

    cells = [
        page.cell_text(1, 1),
        page.cell_text(25, 25),
        page.cell_text(50, 50),
    ]

    for text in cells:
        assert re.fullmatch(r"\d+\.\d+", text), f"Unexpected cell text: {text!r}"
