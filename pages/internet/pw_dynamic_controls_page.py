from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWDynamicControlsPage(PWBasePage):
    URL_PATH = "/dynamic_controls"

    CHECKBOX = "#checkbox"
    TOGGLE_CHECKBOX_BTN = "#checkbox-example button"
    ENABLE_DISABLE_BTN = "#input-example button"
    INPUT_FIELD = "#input-example input"
    MESSAGE = "#message"

    def open(self) -> "PWDynamicControlsPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.ENABLE_DISABLE_BTN)
        return self

    def toggle_checkbox(self) -> "PWDynamicControlsPage":
        self.click(self.TOGGLE_CHECKBOX_BTN)
        self.expect_visible(self.MESSAGE)
        return self

    def is_checkbox_visible(self) -> bool:
        return self.locator(self.CHECKBOX).count() > 0

    def enable_input(self) -> "PWDynamicControlsPage":
        self.click(self.ENABLE_DISABLE_BTN)
        self.expect_visible(self.MESSAGE)
        self.page.wait_for_function(
            "sel => !document.querySelector(sel).disabled",
            arg=self.INPUT_FIELD,
            timeout=self.config.timeout_ms,
        )
        return self

    def disable_input(self) -> "PWDynamicControlsPage":
        self.click(self.ENABLE_DISABLE_BTN)
        self.expect_visible(self.MESSAGE)
        self.page.wait_for_function(
            "sel => document.querySelector(sel).disabled",
            arg=self.INPUT_FIELD,
            timeout=self.config.timeout_ms,
        )
        return self

    def is_input_enabled(self) -> bool:
        return self.locator(self.INPUT_FIELD).is_enabled()

    def message_text(self) -> str:
        return self.get_text(self.MESSAGE)
