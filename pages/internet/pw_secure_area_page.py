from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWSecureAreaPage(PWBasePage):
    HEADER = "#content h2"
    FLASH = "#flash"
    LOGOUT = "a[href='/logout']"

    def wait_loaded(self) -> "PWSecureAreaPage":
        self.expect_visible(self.LOGOUT)
        return self

    def header(self) -> str:
        return self.get_text(self.HEADER)

    def flash_message(self) -> str:
        return self.get_text(self.FLASH)

    def logout(self) -> None:
        self.click(self.LOGOUT)
