from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.core.base_page import BasePage


class RedirectorPage(BasePage):
    URL_PATH = "/redirector"

    HEADING = (By.TAG_NAME, "h3")
    REDIRECT_LINK = (By.ID, "redirect")

    def load(self) -> "RedirectorPage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.HEADING)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def click_redirect(self) -> None:
        self.click(self.REDIRECT_LINK)

    def current_url(self) -> str:
        return self.driver.current_url

    def wait_for_url_contains(self, text: str, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(EC.url_contains(text))
