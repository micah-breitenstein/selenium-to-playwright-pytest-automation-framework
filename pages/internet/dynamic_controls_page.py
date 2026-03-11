from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class DynamicControlsPage(BasePage):
    CHECKBOX = (By.CSS_SELECTOR, "#checkbox")
    TOGGLE_CHECKBOX_BTN = (By.CSS_SELECTOR, "#checkbox-example button")
    ENABLE_DISABLE_BTN = (By.CSS_SELECTOR, "#input-example button")
    INPUT_FIELD = (By.CSS_SELECTOR, "#input-example input")
    MESSAGE = (By.ID, "message")

    def toggle_checkbox(self) -> "DynamicControlsPage":
        self.click(self.TOGGLE_CHECKBOX_BTN)
        self.wait_visible(self.MESSAGE)
        return self

    def is_checkbox_visible(self) -> bool:
        return len(self.find_all(self.CHECKBOX)) > 0

    def enable_input(self) -> "DynamicControlsPage":
        self.click(self.ENABLE_DISABLE_BTN)
        self.wait_visible(self.MESSAGE)
        self.wait.until(lambda d: self.find(self.INPUT_FIELD).is_enabled())
        return self

    def disable_input(self) -> "DynamicControlsPage":
        self.click(self.ENABLE_DISABLE_BTN)
        self.wait_visible(self.MESSAGE)
        self.wait.until(lambda d: not self.find(self.INPUT_FIELD).is_enabled())
        return self

    def is_input_enabled(self) -> bool:
        return self.find(self.INPUT_FIELD).is_enabled()

    def message_text(self) -> str:
        return self.get_text(self.MESSAGE).strip()
