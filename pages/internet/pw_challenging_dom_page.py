from __future__ import annotations

from playwright.sync_api import expect

from pages.core.pw_base_page import PWBasePage


class PWChallengingDomPage(PWBasePage):
    URL_PATH = "/challenging_dom"
    ALL_BTNS = "#content a.button"
    BLUE_BTN = "a.button:not(.alert):not(.success)"
    RED_BTN = "a.button.alert"
    GREEN_BTN = "a.button.success"
    CANVAS = "canvas"
    TABLE_ROWS = "table tbody tr"

    def open(self) -> "PWChallengingDomPage":
        last_exc: Exception | None = None

        for attempt in range(3):
            try:
                self.go(self.URL_PATH)
                self.page.wait_for_load_state(
                    "domcontentloaded", timeout=self.config.timeout_ms
                )
                expect(self.locator(self.CANVAS)).to_be_visible(
                    timeout=self.config.timeout_ms
                )
                expect(self.locator(self.ALL_BTNS)).to_have_count(
                    3, timeout=self.config.timeout_ms
                )
                expect(self.locator(self.TABLE_ROWS)).to_have_count(
                    10, timeout=self.config.timeout_ms
                )
                self.expect_visible(self.BLUE_BTN)
                self.expect_visible(self.RED_BTN)
                self.expect_visible(self.GREEN_BTN)
                return self
            except AssertionError as exc:
                last_exc = exc
                self.log.warning(
                    "Challenging DOM did not become ready on attempt %s/3; retrying",
                    attempt + 1,
                )
                if attempt < 2:
                    self.page.wait_for_timeout(500)

        assert last_exc is not None
        raise last_exc

    def button_texts(self) -> dict[str, str]:
        return {
            "blue": (
                self.locator(self.BLUE_BTN).text_content(timeout=self.config.timeout_ms)
                or ""
            ).strip(),
            "red": (
                self.locator(self.RED_BTN).text_content(timeout=self.config.timeout_ms)
                or ""
            ).strip(),
            "green": (
                self.locator(self.GREEN_BTN).text_content(
                    timeout=self.config.timeout_ms
                )
                or ""
            ).strip(),
        }
