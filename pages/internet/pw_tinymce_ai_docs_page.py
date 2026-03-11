from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWTinyMceAiDocsPage(PWBasePage):
    URL = "https://www.tiny.cloud/docs/tinymce/6/ai/#interactive-example"

    LIVE_DEMO_CONTAINER = "#live-demo_ai > div.content"
    OUTER_IFRAME = "#live-demo_ai > div.content iframe"

    TOOLBAR_BOLD = "button[aria-label='Bold'], button[title='Bold']"
    TOOLBAR_ITALIC = "button[aria-label='Italic'], button[title='Italic']"
    EDIT_IFRAME = "iframe.tox-edit-area__iframe"
    EDITOR_BODY = "body#tinymce"

    def open(self, timeout_ms: int = 60_000) -> "PWTinyMceAiDocsPage":
        self.page.goto(self.URL, wait_until="domcontentloaded", timeout=timeout_ms)
        container = self.page.locator(self.LIVE_DEMO_CONTAINER)
        container.wait_for(state="visible", timeout=timeout_ms)
        container.scroll_into_view_if_needed(timeout=timeout_ms)
        self.page.locator(self.OUTER_IFRAME).first.wait_for(
            state="attached", timeout=timeout_ms
        )
        self._maybe_click_start_overlay(timeout_ms=3_000)
        return self

    def assert_phrase_in_editor(
        self, phrase: str, timeout_ms: int = 20_000
    ) -> "PWTinyMceAiDocsPage":
        demo_body = self.page.frame_locator(self.OUTER_IFRAME).locator("body")
        attempts = max(1, timeout_ms // 1000)
        for _ in range(attempts):
            try:
                body_text = demo_body.inner_text(timeout=1_000)
                if phrase in body_text:
                    return self
            except Exception:
                pass

            if self.is_editor_interactive(timeout_ms=1_000):
                try:
                    editor_text = self._editor_body().inner_text(timeout=1_000)
                    if phrase in editor_text:
                        return self
                except Exception:
                    pass

            self.page.wait_for_timeout(250)

        final_editor_text = ""
        if self.is_editor_interactive(timeout_ms=1_000):
            try:
                final_editor_text = self._editor_body().inner_text(timeout=1_000)
            except Exception:
                final_editor_text = ""

        assert phrase in final_editor_text, f"Could not find phrase in demo: {phrase!r}"
        return self

    def assert_html_contains_any(
        self, needles: list[str], timeout_ms: int = 20_000
    ) -> "PWTinyMceAiDocsPage":
        html = self.editor_html(timeout_ms=timeout_ms)
        assert any(needle in html for needle in needles), (
            f"None of {needles!r} found in editor HTML."
        )
        return self

    def set_plain_text(
        self, text: str, timeout_ms: int = 20_000
    ) -> "PWTinyMceAiDocsPage":
        if not self.is_editor_interactive(timeout_ms=timeout_ms):
            raise RuntimeError("TinyMCE editor is not interactive")
        body = self._editor_body()
        body.click(timeout=timeout_ms)
        body.press("Meta+a", timeout=timeout_ms)
        body.type(text, timeout=timeout_ms)
        return self

    def select_all_in_editor(self, timeout_ms: int = 20_000) -> "PWTinyMceAiDocsPage":
        body = self._editor_body()
        body.click(timeout=timeout_ms)
        body.press("Meta+a", timeout=timeout_ms)
        return self

    def click_bold(self, timeout_ms: int = 20_000) -> "PWTinyMceAiDocsPage":
        self.page.frame_locator(self.OUTER_IFRAME).locator(
            self.TOOLBAR_BOLD
        ).first.click(timeout=timeout_ms)
        return self

    def click_italic(self, timeout_ms: int = 20_000) -> "PWTinyMceAiDocsPage":
        self.page.frame_locator(self.OUTER_IFRAME).locator(
            self.TOOLBAR_ITALIC
        ).first.click(timeout=timeout_ms)
        return self

    def editor_html(self, timeout_ms: int = 20_000) -> str:
        return self._editor_body().evaluate("node => node.innerHTML")

    def is_editor_interactive(self, timeout_ms: int = 10_000) -> bool:
        body = self._editor_body()
        try:
            body.wait_for(state="visible", timeout=timeout_ms)
            contenteditable = body.get_attribute("contenteditable", timeout=timeout_ms)
            if contenteditable == "false":
                return False
            return True
        except Exception:
            return False

    def format_bold(self, text: str, timeout_ms: int = 20_000) -> "PWTinyMceAiDocsPage":
        return (
            self.set_plain_text(text, timeout_ms=timeout_ms)
            .select_all_in_editor(timeout_ms=timeout_ms)
            .click_bold(timeout_ms=timeout_ms)
        )

    def format_italic(
        self, text: str, timeout_ms: int = 20_000
    ) -> "PWTinyMceAiDocsPage":
        return (
            self.set_plain_text(text, timeout_ms=timeout_ms)
            .select_all_in_editor(timeout_ms=timeout_ms)
            .click_italic(timeout_ms=timeout_ms)
        )

    def _maybe_click_start_overlay(self, timeout_ms: int = 3_000) -> bool:
        candidates = [
            "button:has-text('Run')",
            "button:has-text('Start')",
            "button:has-text('Load')",
            "button:has-text('Play')",
            "button[aria-label*='Run']",
        ]
        for selector in candidates:
            locator = self.page.frame_locator(self.OUTER_IFRAME).locator(selector).first
            try:
                if locator.is_visible(timeout=500):
                    locator.click(timeout=timeout_ms)
                    return True
            except Exception:
                continue
        return False

    def _editor_body(self):
        return (
            self.page.frame_locator(self.OUTER_IFRAME)
            .frame_locator(self.EDIT_IFRAME)
            .locator(self.EDITOR_BODY)
        )
