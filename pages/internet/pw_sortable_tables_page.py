from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWSortableTablesPage(PWBasePage):
    URL_PATH = "/tables"
    HEADING = "#content h3"
    TABLE1 = "#table1"
    TABLE2 = "#table2"
    TABLE1_ROWS = "#table1 tbody tr"
    TABLE2_ROWS = "#table2 tbody tr"

    def load(self) -> "PWSortableTablesPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.TABLE1)
        self.expect_visible(self.TABLE2)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def row_count(self, table_id: int = 1) -> int:
        selector = self.TABLE1_ROWS if table_id == 1 else self.TABLE2_ROWS
        return self.locator(selector).count()
