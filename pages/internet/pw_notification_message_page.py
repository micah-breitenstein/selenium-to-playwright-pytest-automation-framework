from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWNotificationMessagePage(PWBasePage):
    URL_PATH = "/notification_message_rendered"
    HEADING = "h3"
    CLICK_HERE = "text=Click here"
    FLASH = "#flash"

    def load(self) -> "PWNotificationMessagePage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def click_to_load_message(self) -> "PWNotificationMessagePage":
        self.click(self.CLICK_HERE)
        self.expect_visible(self.FLASH)
        return self

    def notification_text(self) -> str:
        return self.get_text(self.FLASH)
