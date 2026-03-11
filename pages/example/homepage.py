from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class HomePage(BasePage):
    """
    Generic homepage — can be used as a fallback for any site.
    Demonstrates the BasePage pattern.
    """

    # Locators
    HEADING = (By.TAG_NAME, "h1")

    def load(self) -> "HomePage":
        """Navigate to the site root."""
        self.go("/")
        return self

    def get_heading_text(self) -> str:
        """Return the text of the main heading."""
        return self.get_text(self.HEADING)
