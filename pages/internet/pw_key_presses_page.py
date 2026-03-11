from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWKeyPressesPage(PWBasePage):
    URL_PATH = "/key_presses"
    INPUT = "#target"
    RESULT = "#result"

    def open(self) -> "PWKeyPressesPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.INPUT)
        return self

    def press_and_wait_for(self, key: str, expected: str) -> str:
        expected_text = f"You entered: {expected}"
        target = self.locator(self.INPUT)
        target.click(timeout=self.config.timeout_ms)
        target.press(key, timeout=self.config.timeout_ms)
        self.locator(self.RESULT).wait_for(state="visible", timeout=self.config.timeout_ms)
        self.locator(self.RESULT).filter(has_text=expected_text).wait_for(
            state="visible", timeout=self.config.timeout_ms
        )
        return self.get_text(self.RESULT)
