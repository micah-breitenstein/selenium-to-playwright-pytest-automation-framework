from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class LargeDomPage(BasePage):
    URL_PATH = "/large"

    HEADING = (By.CSS_SELECTOR, "#content h3")
    TABLE = (By.ID, "large-table")
    TABLE_ROWS = (By.CSS_SELECTOR, "#large-table tbody tr")

    def load(self) -> "LargeDomPage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.HEADING)
        self.wait_visible(self.TABLE)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def row_count(self) -> int:
        return len(self.find_all(self.TABLE_ROWS))

    def column_count(self) -> int:
        rows = self.find_all(self.TABLE_ROWS)
        if not rows:
            return 0
        return len(rows[0].find_elements(By.TAG_NAME, "td"))

    def cell_text(self, row_index: int, column_index: int) -> str:
        """
        row_index and column_index are 1-based.
        """
        if row_index < 1 or column_index < 1:
            raise ValueError("row_index and column_index must be >= 1")

        selector = (
            f"#large-table tbody tr:nth-of-type({row_index}) "
            f"td:nth-of-type({column_index})"
        )
        locator = (By.CSS_SELECTOR, selector)
        return self.get_text(locator).strip()

    def element_text_by_id(self, element_id: str) -> str:
        locator = (By.ID, element_id)
        return self.get_text(locator).strip()
