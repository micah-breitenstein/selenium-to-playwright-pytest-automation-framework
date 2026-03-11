from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWStatusCodesPage(PWBasePage):
    URL_PATH = "/status_codes"

    HEADING = "h3"
    RESULT_TEXT = "#content p"
    HERE_LINK = "text=here"

    def load(self) -> "PWStatusCodesPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def click_code(self, code: int) -> "PWStatusCodesPage":
        self.click(f"text={code}")
        self.page.wait_for_url(
            f"**/status_codes/{code}", timeout=self.config.timeout_ms
        )
        self.expect_visible(self.RESULT_TEXT)
        return self

    def result_text(self) -> str:
        return self.get_text(self.RESULT_TEXT)

    def click_here_to_return(self) -> "PWStatusCodesPage":
        self.click(self.HERE_LINK)
        self.page.wait_for_url("**/status_codes", timeout=self.config.timeout_ms)
        self.expect_visible(self.HEADING)
        return self
