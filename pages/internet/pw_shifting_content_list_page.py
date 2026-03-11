from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWShiftingContentListPage(PWBasePage):
    URL_PATH = "/shifting_content/list"
    HEADING = "#content h3"
    LIST_CONTAINER = "#content .row .large-6.columns"
    STATIC_RECORD_TEXT = "Important Information You're Looking For"

    def load(self) -> "PWShiftingContentListPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        self.expect_visible(self.LIST_CONTAINER)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def list_items(self) -> list[str]:
        raw_text = (
            self.locator(self.LIST_CONTAINER).first.inner_text(timeout=self.config.timeout_ms)
            or ""
        ).strip()
        return [line.strip() for line in raw_text.splitlines() if line.strip()]

    def has_static_record(self) -> bool:
        return self.STATIC_RECORD_TEXT in self.list_items()

    def static_record_count(self) -> int:
        return self.list_items().count(self.STATIC_RECORD_TEXT)
