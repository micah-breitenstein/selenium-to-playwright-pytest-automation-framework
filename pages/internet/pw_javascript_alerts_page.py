from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWJavaScriptAlertsPage(PWBasePage):
    URL_PATH = "/javascript_alerts"

    JS_ALERT_BUTTON = "button:has-text('Click for JS Alert')"
    JS_CONFIRM_BUTTON = "button:has-text('Click for JS Confirm')"
    JS_PROMPT_BUTTON = "button:has-text('Click for JS Prompt')"
    RESULT = "#result"

    def open(self) -> "PWJavaScriptAlertsPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.JS_ALERT_BUTTON)
        return self

    def click_js_alert(self) -> "PWJavaScriptAlertsPage":
        self.click(self.JS_ALERT_BUTTON)
        return self

    def click_js_confirm(self) -> "PWJavaScriptAlertsPage":
        self.click(self.JS_CONFIRM_BUTTON)
        return self

    def click_js_prompt(self) -> "PWJavaScriptAlertsPage":
        self.click(self.JS_PROMPT_BUTTON)
        return self

    def accept_next_dialog(self, prompt_text: str | None = None) -> "PWJavaScriptAlertsPage":
        self.page.once("dialog", lambda d: d.accept(prompt_text))
        return self

    def dismiss_next_dialog(self) -> "PWJavaScriptAlertsPage":
        self.page.once("dialog", lambda d: d.dismiss())
        return self

    def result_text(self) -> str:
        return self.get_text(self.RESULT)
