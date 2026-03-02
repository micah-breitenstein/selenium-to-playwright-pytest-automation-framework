from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class IFramePage:
    PATH = "/iframe"
    EDITOR_IFRAME = (By.ID, "mce_0_ifr")
    EDITOR_BODY = (By.ID, "tinymce")

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self, timeout: int = 15) -> "IFramePage":
        self.driver.get(f"{self.base_url}{self.PATH}")
        WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*self.EDITOR_IFRAME))
        return self

    def is_read_only(self, timeout: int = 10) -> bool:
        wait = WebDriverWait(self.driver, timeout)
        iframe = wait.until(lambda d: d.find_element(*self.EDITOR_IFRAME))
        self.driver.switch_to.frame(iframe)
        try:
            body = wait.until(lambda d: d.find_element(*self.EDITOR_BODY))
            contenteditable = body.get_attribute("contenteditable")
            return contenteditable in (None, "false")
        finally:
            self.driver.switch_to.default_content()

    def get_editor_text(self, timeout: int = 15, wait_for_content: bool = False) -> str:
        wait = WebDriverWait(self.driver, timeout)
        iframe = wait.until(lambda d: d.find_element(*self.EDITOR_IFRAME))
        self.driver.switch_to.frame(iframe)
        try:
            body = wait.until(lambda d: d.find_element(*self.EDITOR_BODY))
            if wait_for_content:
                wait.until(lambda d: body.text.strip() != "")
            return body.text
        finally:
            self.driver.switch_to.default_content()

    def set_editor_text(self, text: str, timeout: int = 15) -> "IFramePage":
        wait = WebDriverWait(self.driver, timeout)
        iframe = wait.until(lambda d: d.find_element(*self.EDITOR_IFRAME))
        self.driver.switch_to.frame(iframe)
        try:
            body = wait.until(lambda d: d.find_element(*self.EDITOR_BODY))
            body.click()
            body.send_keys(Keys.COMMAND, "a")
            body.send_keys(text)
            return self
        finally:
            self.driver.switch_to.default_content()