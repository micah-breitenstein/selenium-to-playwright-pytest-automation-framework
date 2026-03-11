from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWInputsPage(PWBasePage):
    URL_PATH = "/inputs"
    NUMBER_INPUT = "#content input[type='number']"

    def open(self) -> "PWInputsPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.NUMBER_INPUT)
        return self

    def value(self) -> str:
        return self.locator(self.NUMBER_INPUT).input_value(
            timeout=self.config.timeout_ms
        )

    def set_number(self, n: int) -> "PWInputsPage":
        self.fill(self.NUMBER_INPUT, str(n))
        return self
