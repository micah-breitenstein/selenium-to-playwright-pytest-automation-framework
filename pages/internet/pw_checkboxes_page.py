from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWCheckboxesPage(PWBasePage):
    URL_PATH = "/checkboxes"
    CB1 = "#checkboxes input:nth-of-type(1)"
    CB2 = "#checkboxes input:nth-of-type(2)"

    def open(self) -> None:
        self.go(self.URL_PATH)
        self.expect_visible(self.CB1)

    def is_checked(self, selector: str) -> bool:
        return self.locator(selector).is_checked(timeout=self.config.timeout_ms)

    def set_checked(self, selector: str, checked: bool) -> None:
        locator = self.locator(selector)
        if locator.is_checked(timeout=self.config.timeout_ms) != checked:
            locator.click(timeout=self.config.timeout_ms)
