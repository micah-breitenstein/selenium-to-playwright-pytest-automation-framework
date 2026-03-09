from __future__ import annotations

from dataclasses import dataclass

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class InputsPage:
    driver: WebDriver
    base_url: str
    timeout: float = 10.0

    PATH = "/inputs"

    # The page has one number input
    NUMBER_INPUT = (By.CSS_SELECTOR, "#content input[type='number']")

    def url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.PATH}"

    def open(self) -> "InputsPage":
        self.driver.get(self.url())
        self.wait_for_loaded()
        return self

    def wait_for_loaded(self) -> None:
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(self.NUMBER_INPUT)
        )

    def input_el(self):
        return self.driver.find_element(*self.NUMBER_INPUT)

    def value(self) -> str:
        # For <input>, read the value attribute (not .text)
        return self.input_el().get_attribute("value") or ""

    def clear(self) -> "InputsPage":
        el = self.input_el()
        el.click()
        # CTRL/CMD + A + Backspace (cross-platform)
        el.send_keys(Keys.COMMAND, "a")
        el.send_keys(Keys.BACKSPACE)
        # If still not empty, retry with CTRL (some drivers ignore COMMAND)
        if self.value():
            el.send_keys(Keys.CONTROL, "a")
            el.send_keys(Keys.BACKSPACE)
        return self

    def set_number(self, n: int) -> "InputsPage":
        self.clear()
        el = self.input_el()
        el.send_keys(str(n))
        return self

    def increment(self, steps: int = 1) -> "InputsPage":
        el = self.input_el()
        el.click()
        for _ in range(max(0, steps)):
            el.send_keys(Keys.ARROW_UP)
        return self

    def decrement(self, steps: int = 1) -> "InputsPage":
        el = self.input_el()
        el.click()
        for _ in range(max(0, steps)):
            el.send_keys(Keys.ARROW_DOWN)
        return self

    def wait_for_value(self, expected: str, timeout: float = 3.0) -> str:
        wait = WebDriverWait(self.driver, timeout)

        def matches(d: WebDriver):
            try:
                v = d.find_element(*self.NUMBER_INPUT).get_attribute("value") or ""
                return v if v == expected else False
            except StaleElementReferenceException:
                return False

        try:
            return str(wait.until(matches))
        except TimeoutException:
            return self.value()
