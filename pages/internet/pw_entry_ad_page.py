from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWEntryAdPage(PWBasePage):
    URL_PATH = "/entry_ad"
    MODAL_CONTENT = "#modal .modal"
    MODAL_TITLE = "#modal .modal-title h3"
    MODAL_CLOSE = "#modal .modal-footer p"

    def open(self) -> "PWEntryAdPage":
        self.go(self.URL_PATH)
        return self

    def modal_is_visible(self, timeout_ms: int = 2000) -> bool:
        try:
            self.locator(self.MODAL_CONTENT).wait_for(state="visible", timeout=timeout_ms)
            return True
        except Exception:
            return False

    def modal_title(self, timeout_ms: int = 3000) -> str:
        try:
            text = self.locator(self.MODAL_TITLE).text_content(timeout=timeout_ms)
            return (text or "").strip()
        except Exception:
            return ""

    def close_modal(self) -> "PWEntryAdPage":
        self.locator(self.MODAL_CLOSE).click(timeout=self.config.timeout_ms)
        self.locator(self.MODAL_CONTENT).wait_for(
            state="hidden", timeout=self.config.timeout_ms
        )
        return self
