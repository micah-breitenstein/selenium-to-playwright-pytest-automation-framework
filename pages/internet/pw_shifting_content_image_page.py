from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWShiftingContentImagePage(PWBasePage):
    URL_PATH = "/shifting_content/image"
    HEADING = "#content h3"
    IMAGE = "#content img"

    def load(self) -> "PWShiftingContentImagePage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        self.expect_visible(self.IMAGE)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def image_src(self) -> str:
        return (
            self.locator(self.IMAGE).first.get_attribute(
                "src", timeout=self.config.timeout_ms
            )
            or ""
        )
