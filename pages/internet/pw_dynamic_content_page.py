from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWDynamicContentPage(PWBasePage):
    URL_PATH = "/dynamic_content"
    ALL_ROWS = "#content .row"
    ROW_TEXT = ".large-10"

    def open_page(self, static: bool = False) -> "PWDynamicContentPage":
        path = self.URL_PATH + ("?with_content=static" if static else "")
        self.go(path)
        self.locator(self.ALL_ROWS).first.wait_for(
            state="visible", timeout=self.config.timeout_ms
        )
        return self

    def rows_text(self) -> list[str]:
        texts: list[str] = []
        rows = self.locator(self.ALL_ROWS)
        for index in range(rows.count()):
            text = (
                rows.nth(index)
                .locator(self.ROW_TEXT)
                .first.text_content(timeout=self.config.timeout_ms)
                or ""
            ).strip()
            if text:
                texts.append(text)
        return texts

    def refresh(self) -> "PWDynamicContentPage":
        self.page.reload(wait_until="domcontentloaded", timeout=self.config.timeout_ms)
        self.locator(self.ALL_ROWS).first.wait_for(
            state="visible", timeout=self.config.timeout_ms
        )
        return self

    def row_count(self) -> int:
        return len(self.rows_text())
