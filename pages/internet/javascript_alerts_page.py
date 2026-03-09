from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class JavaScriptAlertsPage:
    driver: WebDriver
    base_url: str
    timeout: int = 10

    PATH = "/javascript_alerts"

    JS_ALERT_BUTTON = (By.XPATH, "//button[text()='Click for JS Alert']")
    JS_CONFIRM_BUTTON = (By.XPATH, "//button[text()='Click for JS Confirm']")
    JS_PROMPT_BUTTON = (By.XPATH, "//button[text()='Click for JS Prompt']")

    RESULT = (By.ID, "result")

    def url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.PATH}"

    def open(self) -> "JavaScriptAlertsPage":
        self.driver.get(self.url())
        return self

    def click_js_alert(self) -> None:
        self.driver.find_element(*self.JS_ALERT_BUTTON).click()

    def click_js_confirm(self) -> None:
        self.driver.find_element(*self.JS_CONFIRM_BUTTON).click()

    def click_js_prompt(self) -> None:
        self.driver.find_element(*self.JS_PROMPT_BUTTON).click()

    def accept_alert(self) -> None:
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        alert.accept()

    def dismiss_alert(self) -> None:
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        alert.dismiss()

    def send_text_to_prompt(self, text: str) -> None:
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        alert.send_keys(text)
        alert.accept()

    def result_text(self) -> str:
        return self.driver.find_element(*self.RESULT).text
