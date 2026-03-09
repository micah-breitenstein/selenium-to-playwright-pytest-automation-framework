from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.core.base_page import BasePage


class SlowResourcesPage(BasePage):
    URL_PATH = "/slow"

    HEADING = (By.CSS_SELECTOR, "#content h3")
    DESCRIPTION = (By.CSS_SELECTOR, "#content .example p")

    # JS snippet: returns True when jQuery has no active AJAX requests
    _AJAX_DONE_JS = "return (typeof jQuery !== 'undefined') && (jQuery.active === 0);"

    def _wait_for_ajax(self, timeout: int = 45) -> None:
        """Wait until the background $.get('/slow_external') finishes."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script(self._AJAX_DONE_JS)
        )

    def load(self, timeout: int = 45) -> "SlowResourcesPage":
        """
        Load the page and wait for the slow background AJAX request to finish.
        The page fires $.get('/slow_external') which takes ~30 seconds.
        """
        self.go(self.URL_PATH)
        self._wait_for_ajax(timeout)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def description_text(self) -> str:
        return self.get_text(self.DESCRIPTION).strip()

    def page_load_time(self, timeout: int = 45) -> float:
        """
        Navigate to the page and return the wall-clock seconds until
        the background AJAX request completes.
        """
        start = time.time()
        self.go(self.URL_PATH)
        self._wait_for_ajax(timeout)
        return time.time() - start

    def current_url(self) -> str:
        return self.driver.current_url
