from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class DynamicControlsPage(BasePage):
    CHECKBOX = (By.CSS_SELECTOR, "#checkbox")
    TOGGLE_CHECKBOX_BTN = (By.CSS_SELECTOR, "#checkbox-example button")
    ENABLE_DISABLE_BTN = (By.CSS_SELECTOR, "#input-example button")
    INPUT_FIELD = (By.CSS_SELECTOR, "#input-example input")

    def enable_input(self) -> "DynamicControlsPage":
        self.click(self.ENABLE_DISABLE_BTN)
        self.wait.until(lambda d: self.find(self.INPUT_FIELD).is_enabled())
        return self

    def disable_input(self) -> "DynamicControlsPage":
        self.click(self.ENABLE_DISABLE_BTN)
        self.wait.until(lambda d: not self.find(self.INPUT_FIELD).is_enabled())
        return self

    def is_input_enabled(self) -> bool:
        return self.find(self.INPUT_FIELD).is_enabled()
