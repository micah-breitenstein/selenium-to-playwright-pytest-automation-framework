from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class ShiftingContentListPage(BasePage):
    URL_PATH = "/shifting_content/list"

    HEADING = (By.CSS_SELECTOR, "#content h3")
    # Items are plain text separated by <br> inside a single container div
    LIST_CONTAINER = (By.CSS_SELECTOR, "#content .row .large-6.columns")

    STATIC_RECORD_TEXT = "Important Information You're Looking For"

    def load(self) -> "ShiftingContentListPage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def refresh(self) -> "ShiftingContentListPage":
        self.driver.refresh()
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.HEADING)
        self.wait_visible(self.LIST_CONTAINER)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def list_items(self) -> list[str]:
        """
        The page renders items as plain text separated by <br> tags
        inside a single container div. Split on newlines to get individual items.
        """
        container = self.find(self.LIST_CONTAINER)
        raw_text = (container.text or "").strip()
        return [line.strip() for line in raw_text.splitlines() if line.strip()]

    def has_static_record(self) -> bool:
        return self.STATIC_RECORD_TEXT in self.list_items()

    def static_record_count(self) -> int:
        return self.list_items().count(self.STATIC_RECORD_TEXT)

    def static_record_index(self) -> int:
        """
        Return 0-based index of the static record in the visible list.
        Returns -1 if not found.
        """
        items = self.list_items()
        try:
            return items.index(self.STATIC_RECORD_TEXT)
        except ValueError:
            return -1

    def current_url(self) -> str:
        return self.driver.current_url
