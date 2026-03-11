from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWShadowDomPage(PWBasePage):
    URL_PATH = "/shadowdom"
    HEADING = "h1"
    SHADOW_HOST = "my-paragraph"

    def load(self) -> "PWShadowDomPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def shadow_host_count(self) -> int:
        return self.locator(self.SHADOW_HOST).count()
