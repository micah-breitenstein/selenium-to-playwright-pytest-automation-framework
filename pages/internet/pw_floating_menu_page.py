from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWFloatingMenuPage(PWBasePage):
    URL_PATH = "/floating_menu"
    MENU = "#menu"
    MENU_LINKS = "#menu a"

    def open(self) -> "PWFloatingMenuPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.MENU)
        return self

    def menu_is_displayed(self) -> bool:
        return self.locator(self.MENU).is_visible(timeout=self.config.timeout_ms)

    def click_menu_item(self, text: str) -> None:
        links = self.locator(self.MENU_LINKS)
        count = links.count()
        for index in range(count):
            link = links.nth(index)
            if (
                link.text_content(timeout=self.config.timeout_ms) or ""
            ).strip().lower() == text.strip().lower():
                link.click(timeout=self.config.timeout_ms)
                return
        raise AssertionError(f"Menu item not found: {text!r}")

    def current_hash(self) -> str:
        return self.page.evaluate("window.location.hash") or ""

    def scroll_to_bottom(self) -> None:
        self.page.evaluate(
            """
            window.scrollTo(0, Math.max(
                document.body.scrollHeight,
                document.documentElement.scrollHeight
            ));
            """
        )
