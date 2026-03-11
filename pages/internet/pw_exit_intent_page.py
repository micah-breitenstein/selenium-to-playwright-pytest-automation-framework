from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWExitIntentPage(PWBasePage):
    URL_PATH = "/exit_intent"
    MODAL = ".modal"
    MODAL_TITLE = ".modal-title h3"
    MODAL_CLOSE = ".modal-footer p"

    def open(self) -> "PWExitIntentPage":
        self.go(self.URL_PATH)
        self.page.wait_for_function(
            "() => document.readyState === 'complete'",
            timeout=self.config.timeout_ms,
        )
        return self

    def trigger_exit_intent(self) -> "PWExitIntentPage":
        self.page.evaluate(
            """() => {
                const el = document.documentElement;
                const opts = { bubbles: true, cancelable: true, view: window,
                               clientX: 0, clientY: 0, relatedTarget: null };
                el.dispatchEvent(new MouseEvent('mouseout', opts));
                el.dispatchEvent(new MouseEvent('mouseleave', opts));
            }"""
        )
        return self

    def wait_for_modal(self, timeout_ms: int | None = None) -> "PWExitIntentPage":
        ms = timeout_ms if timeout_ms is not None else self.config.timeout_ms
        self.locator(self.MODAL).wait_for(state="visible", timeout=ms)
        return self

    def modal_is_visible(self, timeout_ms: int = 2_000) -> bool:
        try:
            self.locator(self.MODAL).wait_for(state="visible", timeout=timeout_ms)
            return True
        except Exception:
            return False

    def modal_title(self) -> str:
        text = self.locator(self.MODAL_TITLE).text_content(timeout=self.config.timeout_ms)
        return (text or "").strip()

    def close_modal(self) -> "PWExitIntentPage":
        self.locator(self.MODAL_CLOSE).click(timeout=self.config.timeout_ms)
        self.locator(self.MODAL).wait_for(state="hidden", timeout=self.config.timeout_ms)
        return self
