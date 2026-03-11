from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWChallengingDomPage(PWBasePage):
    URL_PATH = "/challenging_dom"
    BLUE_BTN = "a.button:not(.alert):not(.success)"
    RED_BTN = "a.button.alert"
    GREEN_BTN = "a.button.success"

    def open(self) -> "PWChallengingDomPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.BLUE_BTN)
        self.expect_visible(self.RED_BTN)
        self.expect_visible(self.GREEN_BTN)
        return self

    def button_texts(self) -> dict[str, str]:
        return {
            "blue": (self.locator(self.BLUE_BTN).text_content(timeout=self.config.timeout_ms) or "").strip(),
            "red": (self.locator(self.RED_BTN).text_content(timeout=self.config.timeout_ms) or "").strip(),
            "green": (self.locator(self.GREEN_BTN).text_content(timeout=self.config.timeout_ms) or "").strip(),
        }
