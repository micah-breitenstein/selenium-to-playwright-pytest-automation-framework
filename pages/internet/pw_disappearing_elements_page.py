from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWDisappearingElementsPage(PWBasePage):
    URL_PATH = "/disappearing_elements"
    MENU_LINKS = "ul li a"

    def open(self) -> "PWDisappearingElementsPage":
        self.go(self.URL_PATH)
        self.locator(self.MENU_LINKS).first.wait_for(
            state="visible", timeout=self.config.timeout_ms
        )
        return self

    def menu_texts(self) -> list[str]:
        return [text.strip() for text in self.locator(self.MENU_LINKS).all_inner_texts() if text.strip()]

    def has_menu_item(self, label: str) -> bool:
        return label in self.menu_texts()

    def refresh(self) -> "PWDisappearingElementsPage":
        self.page.reload(wait_until="domcontentloaded", timeout=self.config.timeout_ms)
        self.locator(self.MENU_LINKS).first.wait_for(
            state="visible", timeout=self.config.timeout_ms
        )
        return self
