from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWLargeDomPage(PWBasePage):
    URL_PATH = "/large"
    HEADING = "#content h3"
    TABLE = "#large-table"
    TABLE_ROWS = "#large-table tbody tr"

    def load(self) -> "PWLargeDomPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        self.expect_visible(self.TABLE)
        return self

    def row_count(self) -> int:
        return self.locator(self.TABLE_ROWS).count()

    def column_count(self) -> int:
        rows = self.locator(self.TABLE_ROWS)
        if rows.count() == 0:
            return 0
        return rows.nth(0).locator("td").count()
