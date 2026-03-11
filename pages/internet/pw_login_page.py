from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWLoginPage(PWBasePage):
    URL_PATH = "/login"
    USERNAME = "#username"
    PASSWORD = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    FLASH = "#flash"

    def load(self) -> "PWLoginPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.USERNAME)
        return self

    def login_expect_failure(self, username: str, password: str) -> "PWLoginPage":
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        self.expect_visible(self.FLASH)
        return self

    def flash_message(self) -> str:
        return self.get_text(self.FLASH)
