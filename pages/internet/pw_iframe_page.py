from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWIFramePage(PWBasePage):
    URL_PATH = "/iframe"
    EDITOR_IFRAME = "#mce_0_ifr"
    EDITOR_BODY = "#tinymce"

    def open(self) -> "PWIFramePage":
        self.go(self.URL_PATH)
        self.expect_visible(self.EDITOR_IFRAME)
        return self

    def _editor_body(self):
        return self.page.frame_locator(self.EDITOR_IFRAME).locator(self.EDITOR_BODY)

    def is_read_only(self) -> bool:
        value = self._editor_body().get_attribute("contenteditable", timeout=self.config.timeout_ms)
        return value in (None, "false")

    def get_editor_text(self, wait_for_content: bool = False) -> str:
        body = self._editor_body()
        if wait_for_content:
            self.page.wait_for_function(
                "([frameSel, bodySel]) => {"
                " const frame = document.querySelector(frameSel);"
                " const doc = frame?.contentDocument;"
                " const body = doc?.querySelector(bodySel);"
                " return !!body && (body.textContent || '').trim().length > 0;"
                "}",
                arg=[self.EDITOR_IFRAME, self.EDITOR_BODY],
                timeout=self.config.timeout_ms,
            )
        return (body.inner_text(timeout=self.config.timeout_ms) or "").strip()

    def set_editor_text(self, text: str) -> "PWIFramePage":
        body = self._editor_body()
        body.click(timeout=self.config.timeout_ms)
        body.press("Meta+a", timeout=self.config.timeout_ms)
        body.type(text, timeout=self.config.timeout_ms)
        return self
