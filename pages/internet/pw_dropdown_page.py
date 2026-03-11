from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWDropdownPage(PWBasePage):
    URL_PATH = "/dropdown"
    DROPDOWN = "#dropdown"

    def open(self) -> None:
        self.go(self.URL_PATH)
        self.expect_visible(self.DROPDOWN)

    def selected_text(self) -> str:
        text = self.locator(f"{self.DROPDOWN} option:checked").text_content(
            timeout=self.config.timeout_ms
        )
        return (text or "").strip()

    def select_by_visible_text(self, text: str) -> None:
        self.locator(self.DROPDOWN).select_option(label=text, timeout=self.config.timeout_ms)

    def select_by_value(self, value: str) -> None:
        self.locator(self.DROPDOWN).select_option(value=value, timeout=self.config.timeout_ms)
