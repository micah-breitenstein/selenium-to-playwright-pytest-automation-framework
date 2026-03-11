from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWDynamicLoadingPage(PWBasePage):
    URL_PATH = "/dynamic_loading"
    EXAMPLE_2 = "text=Example 2"
    START_BTN = "#start button"
    LOADING = "#loading"
    FINISH = "#finish"

    def open(self) -> "PWDynamicLoadingPage":
        self.go(self.URL_PATH)
        return self

    def open_example_2(self) -> "PWDynamicLoadingPage":
        self.click(self.EXAMPLE_2)
        return self

    def start_loading(self) -> "PWDynamicLoadingPage":
        self.click(self.START_BTN)
        self.locator(self.LOADING).wait_for(state="hidden", timeout=self.config.timeout_ms)
        self.expect_visible(self.FINISH)
        return self

    def finish_text(self) -> str:
        return self.get_text(self.FINISH)
