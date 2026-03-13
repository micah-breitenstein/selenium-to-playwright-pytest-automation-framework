from __future__ import annotations

from playwright.sync_api import expect

from pages.core.pw_base_page import PWBasePage


class PWAddRemoveElementsPage(PWBasePage):
    URL_PATH = "/add_remove_elements/"
    ADD_BUTTON = "button[onclick='addElement()']"
    DELETE_BUTTONS = "button.added-manually"

    def open(self) -> None:
        self.go(self.URL_PATH)
        self.expect_visible(self.ADD_BUTTON)

    def add_element(self, times: int = 1, wait_ms: int = 50) -> None:
        button = self.locator(self.ADD_BUTTON)
        for _ in range(times):
            button.click(timeout=self.config.timeout_ms)
            if wait_ms:
                self.page.wait_for_timeout(wait_ms)

    def delete_count(self) -> int:
        return self.locator(self.DELETE_BUTTONS).count()

    def wait_for_delete_count(self, expected: int) -> None:
        expect(self.locator(self.DELETE_BUTTONS)).to_have_count(
            expected, timeout=self.config.timeout_ms
        )

    def click_delete_at_index(self, index: int = 0) -> None:
        buttons = self.locator(self.DELETE_BUTTONS)
        count = buttons.count()
        if index < 0 or index >= count:
            raise IndexError(
                f"Delete button index {index} out of range (count={count})"
            )
        buttons.nth(index).click(timeout=self.config.timeout_ms)
