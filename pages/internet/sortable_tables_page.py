from __future__ import annotations

import time

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class SortableTablesPage(BasePage):
    URL_PATH = "/tables"

    HEADING = (By.CSS_SELECTOR, "#content h3")

    # Table 1 — no class/ID on cells
    TABLE1 = (By.ID, "table1")
    TABLE1_HEADERS = (By.CSS_SELECTOR, "#table1 thead th span")
    TABLE1_ROWS = (By.CSS_SELECTOR, "#table1 tbody tr")

    # Table 2 — class attributes on cells
    TABLE2 = (By.ID, "table2")
    TABLE2_HEADERS = (By.CSS_SELECTOR, "#table2 thead th span")
    TABLE2_ROWS = (By.CSS_SELECTOR, "#table2 tbody tr")

    # Column name → 0-based index mapping
    COLUMNS = {
        "Last Name": 0,
        "First Name": 1,
        "Email": 2,
        "Due": 3,
        "Web Site": 4,
        "Action": 5,
    }

    def load(self) -> "SortableTablesPage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.TABLE1)
        self.wait_visible(self.TABLE2)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    # -------------------------
    # Generic table helpers
    # -------------------------

    def _header_elements(self, table_id: int):
        locator = self.TABLE1_HEADERS if table_id == 1 else self.TABLE2_HEADERS
        return self.find_all(locator)

    def _row_elements(self, table_id: int):
        locator = self.TABLE1_ROWS if table_id == 1 else self.TABLE2_ROWS
        return self.find_all(locator)

    def header_texts(self, table_id: int = 1) -> list[str]:
        return [h.text.strip() for h in self._header_elements(table_id)]

    def column_values(self, column_name: str, table_id: int = 1) -> list[str]:
        """Return all cell values for a given column name."""
        col_idx = self.COLUMNS[column_name]
        rows = self._row_elements(table_id)
        values: list[str] = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if col_idx < len(cells):
                values.append(cells[col_idx].text.strip())
        return values

    def row_count(self, table_id: int = 1) -> int:
        return len(self._row_elements(table_id))

    # -------------------------
    # Sorting
    # -------------------------

    def sort_by(self, column_name: str, table_id: int = 1) -> None:
        """Click a column header to sort. Click twice for descending."""
        headers = self._header_elements(table_id)
        col_idx = self.COLUMNS[column_name]
        header = headers[col_idx]
        header.click()
        # Brief pause for tablesorter animation
        time.sleep(0.3)

    def sort_ascending(self, column_name: str, table_id: int = 1) -> list[str]:
        """Sort column ascending (one click) and return the resulting values."""
        self.sort_by(column_name, table_id)
        return self.column_values(column_name, table_id)

    def sort_descending(self, column_name: str, table_id: int = 1) -> list[str]:
        """Sort column descending (two clicks) and return the resulting values."""
        self.sort_by(column_name, table_id)
        self.sort_by(column_name, table_id)
        return self.column_values(column_name, table_id)

    # -------------------------
    # Row action links
    # -------------------------

    def _action_cell(self, row: int, table_id: int = 1):
        """Return the Action <td> for a 0-based row index."""
        rows = self._row_elements(table_id)
        cells = rows[row].find_elements(By.TAG_NAME, "td")
        return cells[self.COLUMNS["Action"]]

    def click_edit(self, row: int = 0, table_id: int = 1) -> str:
        """Click the 'edit' link in the given row and return the current URL."""
        cell = self._action_cell(row, table_id)
        cell.find_element(By.LINK_TEXT, "edit").click()
        return self.driver.current_url

    def click_delete(self, row: int = 0, table_id: int = 1) -> str:
        """Click the 'delete' link in the given row and return the current URL."""
        cell = self._action_cell(row, table_id)
        cell.find_element(By.LINK_TEXT, "delete").click()
        return self.driver.current_url
