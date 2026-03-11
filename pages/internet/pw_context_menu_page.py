from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWContextMenuPage(PWBasePage):
    URL_PATH = "/context_menu"
    HOT_SPOT = "#hot-spot"

    def open(self) -> "PWContextMenuPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HOT_SPOT)
        return self

    def context_click_hotspot_and_accept_alert(self) -> str:
        dialog_message: list[str] = []

        def _handle_dialog(dialog):
            dialog_message.append(dialog.message)
            dialog.accept()

        self.page.once("dialog", _handle_dialog)
        self.locator(self.HOT_SPOT).click(
            button="right", timeout=self.config.timeout_ms
        )
        self.page.wait_for_timeout(100)
        return dialog_message[0] if dialog_message else ""
