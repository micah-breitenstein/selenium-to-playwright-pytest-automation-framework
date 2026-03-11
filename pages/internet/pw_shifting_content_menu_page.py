from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWShiftingContentMenuPage(PWBasePage):
    URL_PATH = "/shifting_content/menu"
    HEADING = "#content h3"
    MENU_LINKS = "#content ul li a"

    def load(self) -> "PWShiftingContentMenuPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        self.locator(self.MENU_LINKS).first.wait_for(
            state="visible", timeout=self.config.timeout_ms
        )
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def menu_items(self) -> list[str]:
        return [
            text.strip()
            for text in self.locator(self.MENU_LINKS).all_inner_texts()
            if text.strip()
        ]
