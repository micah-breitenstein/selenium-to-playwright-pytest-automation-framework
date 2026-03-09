from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class NotificationMessagePage(BasePage):
    URL_PATH = "/notification_message_rendered"

    HEADING = (By.TAG_NAME, "h3")
    CLICK_HERE = (By.LINK_TEXT, "Click here")
    FLASH = (By.ID, "flash")

    def load(self) -> "NotificationMessagePage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.HEADING)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def click_to_load_message(self) -> "NotificationMessagePage":
        self.click(self.CLICK_HERE)
        self.wait_visible(self.FLASH)
        return self

    def notification_text(self) -> str:
        return self.get_text(self.FLASH).strip()
