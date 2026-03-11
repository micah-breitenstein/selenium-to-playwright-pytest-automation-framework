from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWRedirectorPage(PWBasePage):
    URL_PATH = "/redirector"
    HEADING = "h3"
    REDIRECT_LINK = "#redirect"

    def load(self) -> "PWRedirectorPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def click_redirect(self) -> None:
        self.click(self.REDIRECT_LINK)

    def wait_for_url_contains(self, text: str) -> None:
        self.page.wait_for_url(f"**/*{text}*", timeout=self.config.timeout_ms)
