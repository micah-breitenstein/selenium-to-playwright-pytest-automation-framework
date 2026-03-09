from __future__ import annotations

from dataclasses import dataclass

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class KeyPressesPage:
    driver: WebDriver
    base_url: str
    timeout: float = 20.0
    poll: float = 0.1

    PATH = "/key_presses"

    INPUT = (By.ID, "target")
    RESULT = (By.ID, "result")

    def url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.PATH}"

    def open(self) -> "KeyPressesPage":
        self.driver.get(self.url())
        WebDriverWait(self.driver, self.timeout, poll_frequency=self.poll).until(
            EC.presence_of_element_located(self.INPUT)
        )
        return self

    def _input_el(self):
        return self.driver.find_element(*self.INPUT)

    def _dispatch_enter_js(self, el) -> None:
        # Dispatch keydown/keyup on the input (bubbles) without triggering default form actions.
        self.driver.execute_script(
            """
            const el = arguments[0];
            el.focus();

            const down = new KeyboardEvent('keydown', {
              key: 'Enter',
              code: 'Enter',
              keyCode: 13,
              which: 13,
              bubbles: true
            });
            const up = new KeyboardEvent('keyup', {
              key: 'Enter',
              code: 'Enter',
              keyCode: 13,
              which: 13,
              bubbles: true
            });

            el.dispatchEvent(down);
            el.dispatchEvent(up);
            """,
            el,
        )

    def press(self, key) -> None:
        """
        Send a key to the target input.

        ENTER is handled via JS event dispatch to avoid odd default actions.
        Other special keys use Actions. Normal characters use send_keys.
        """
        el = self._input_el()
        el.click()

        # Normal characters
        if isinstance(key, str) and len(key) == 1:
            el.send_keys(key)
            return

        # ENTER/RETURN (problem child)
        if key in (Keys.ENTER, Keys.RETURN):
            self._dispatch_enter_js(el)
            return

        # Other special keys
        ActionChains(self.driver).send_keys_to_element(el, key).perform()

    def press_and_wait_for(self, key, expected: str) -> str:
        """
        Press a key and return the exact result line once it matches.
        """
        expected_text = f"You entered: {expected}"

        self.press(key)

        def _get_if_match(d: WebDriver):
            try:
                text = d.find_element(*self.RESULT).text.strip()
                return text if text == expected_text else False
            except StaleElementReferenceException:
                return False

        # IMPORTANT: return the matched text from the wait (no re-read afterward)
        return WebDriverWait(self.driver, self.timeout, poll_frequency=self.poll).until(
            _get_if_match
        )
