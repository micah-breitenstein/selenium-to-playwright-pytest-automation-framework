from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWJavaScriptErrorPage(PWBasePage):
    URL_PATH = "/javascript_error"
    BODY = "body"

    def load(self) -> "PWJavaScriptErrorPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.BODY)
        return self

    def body_text(self) -> str:
        return self.get_text(self.BODY)
