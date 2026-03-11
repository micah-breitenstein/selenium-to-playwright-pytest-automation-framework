from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWABTestPage(PWBasePage):
    URL_PATH = "/abtest"
    HEADER = "h3"

    ALLOWED_HEADERS = {
        "No A/B Test",
        "A/B Test Variation 1",
        "A/B Test Control",
    }

    def open(self) -> None:
        self.go(self.URL_PATH)

    def header_text(self) -> str:
        return self.get_text(self.HEADER)

    def assert_header_is_valid(self) -> None:
        actual = self.header_text()
        assert actual in self.ALLOWED_HEADERS, (
            f"Unexpected header '{actual}'. Expected one of: {sorted(self.ALLOWED_HEADERS)}"
        )
