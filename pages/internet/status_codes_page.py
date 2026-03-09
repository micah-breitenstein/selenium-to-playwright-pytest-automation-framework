from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.core.base_page import BasePage


class StatusCodesPage(BasePage):
    URL_PATH = "/status_codes"

    HEADING = (By.TAG_NAME, "h3")
    CODE_200 = (By.LINK_TEXT, "200")
    CODE_301 = (By.LINK_TEXT, "301")
    CODE_404 = (By.LINK_TEXT, "404")
    CODE_500 = (By.LINK_TEXT, "500")
    RESULT_TEXT = (By.CSS_SELECTOR, "#content p")
    HERE_LINK = (By.LINK_TEXT, "here")

    def load(self) -> "StatusCodesPage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.HEADING)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def click_code(self, code: int) -> "StatusCodesPage":
        locator = (By.LINK_TEXT, str(code))
        # Grab the current <p> so we can detect when the page actually reloads
        old_p = self.driver.find_element(*self.RESULT_TEXT)
        self.click(locator)
        # Wait for old element to go stale (proves DOM reloaded)
        WebDriverWait(self.driver, 10).until(EC.staleness_of(old_p))
        # Now wait for the new page's content
        WebDriverWait(self.driver, 10).until(EC.url_contains(f"/status_codes/{code}"))
        self.wait_visible(self.RESULT_TEXT)
        return self

    def result_text(self) -> str:
        return self.get_text(self.RESULT_TEXT).strip()

    def current_url(self) -> str:
        return self.driver.current_url

    def click_here_to_return(self) -> "StatusCodesPage":
        # Grab old content element to detect page reload
        old_p = self.driver.find_element(*self.RESULT_TEXT)
        self.click(self.HERE_LINK)
        # Wait for old element to go stale (proves DOM reloaded)
        WebDriverWait(self.driver, 10).until(EC.staleness_of(old_p))
        self.wait_for_ready()
        return self

    def wait_for_url_contains(self, text: str, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(EC.url_contains(text))
