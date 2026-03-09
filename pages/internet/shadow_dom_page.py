from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class ShadowDomPage(BasePage):
    URL_PATH = "/shadowdom"

    HEADING = (By.TAG_NAME, "h1")
    SHADOW_HOST = (By.TAG_NAME, "my-paragraph")

    def load(self) -> "ShadowDomPage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.HEADING)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def get_shadow_root(self, index: int = 0):
        """
        Get the shadow root of a shadow host element.
        index: which my-paragraph element (0-based)
        """
        hosts = self.find_all(self.SHADOW_HOST)
        if index >= len(hosts):
            raise IndexError(f"Shadow host index {index} out of range (found {len(hosts)})")
        return hosts[index].shadow_root

    def get_shadow_text(self, index: int = 0) -> str:
        """
        Get text content from within a shadow DOM.
        The shadow DOM contains a <slot> with text.
        """
        shadow_root = self.get_shadow_root(index)
        # Find the slot element inside shadow root
        slot = shadow_root.find_element(By.CSS_SELECTOR, "slot")
        # Get assigned nodes text or slot's own content
        return slot.text.strip() if slot.text else ""

    def get_shadow_slot_content(self, index: int = 0) -> str:
        """
        Get the light DOM content that's slotted into the shadow DOM.
        """
        hosts = self.find_all(self.SHADOW_HOST)
        if index >= len(hosts):
            raise IndexError(f"Shadow host index {index} out of range")
        # The slotted content is in the light DOM (direct children of host)
        return hosts[index].text.strip()

    def shadow_host_count(self) -> int:
        """Return the number of shadow host elements on the page."""
        return len(self.find_all(self.SHADOW_HOST))
