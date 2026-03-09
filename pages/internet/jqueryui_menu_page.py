from __future__ import annotations

import time
from dataclasses import dataclass

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class JQueryUIMenuPage:
    driver: WebDriver
    base_url: str
    timeout: float = 10.0
    poll: float = 0.1

    PATH = "/jqueryui/menu"

    MENU = (By.ID, "menu")

    ENABLED = (By.XPATH, "//*[@id='menu']//a[normalize-space()='Enabled']")
    DOWNLOADS = (By.XPATH, "//*[@id='menu']//a[normalize-space()='Downloads']")

    PDF = (By.XPATH, "//*[@id='menu']//a[normalize-space()='PDF']")
    CSV = (By.XPATH, "//*[@id='menu']//a[normalize-space()='CSV']")
    EXCEL = (By.XPATH, "//*[@id='menu']//a[normalize-space()='Excel']")

    BACK_TO_JQUERY = (
        By.XPATH,
        "//*[@id='menu']//a[normalize-space()='Back to JQuery UI']",
    )

    def url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.PATH}"

    def open(self) -> "JQueryUIMenuPage":
        self.driver.get(self.url())
        WebDriverWait(self.driver, self.timeout, poll_frequency=self.poll).until(
            EC.presence_of_element_located(self.MENU)
        )
        return self

    def _visible(self, locator, timeout: float | None = None):
        t = self.timeout if timeout is None else timeout
        wait = WebDriverWait(self.driver, t, poll_frequency=self.poll)

        def _find_visible(d: WebDriver):
            els = d.find_elements(*locator)
            for el in els:
                try:
                    if el.is_displayed():
                        return el
                except Exception:
                    continue
            return False

        return wait.until(_find_visible)

    def _click(self, locator, timeout: float | None = None) -> None:
        el = self._visible(locator, timeout=timeout)
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    def _hover(self, locator, timeout: float | None = None) -> None:
        el = self._visible(locator, timeout=timeout)
        ActionChains(self.driver).move_to_element(el).pause(0.15).perform()

    def open_downloads_menu(self) -> None:
        self._hover(self.ENABLED, timeout=15)
        time.sleep(0.3)
        self._hover(self.DOWNLOADS, timeout=15)
        time.sleep(0.3)

    def _get_href(self, locator, timeout: float | None = None) -> str:
        el = self._visible(locator, timeout=timeout)
        href = el.get_attribute("href")
        if not href:
            raise AssertionError(f"No href attribute found for locator: {locator}")
        return href

    def _download_href_with_retry(self, locator, retries: int = 3) -> str:
        """Open the Downloads submenu, click the target link, return its href.

        Retries the full hover→click sequence on failure because the jQuery UI
        submenu can collapse between steps, especially under parallel load.
        """
        last_exc: Exception | None = None
        for attempt in range(retries):
            try:
                self.open_downloads_menu()
                el = self._visible(locator, timeout=5)
                href = el.get_attribute("href")
                if href:
                    return href
            except (TimeoutException, Exception) as exc:
                last_exc = exc
            # Reset by moving away from the menu before retrying
            ActionChains(self.driver).move_by_offset(-200, -200).perform()
            time.sleep(0.5)
        raise TimeoutException(
            f"Could not get href for {locator} after {retries} attempts"
        ) from last_exc

    # ---- Public actions that return hrefs ----
    def pdf_href(self) -> str:
        return self._download_href_with_retry(self.PDF)

    def csv_href(self) -> str:
        return self._download_href_with_retry(self.CSV)

    def excel_href(self) -> str:
        return self._download_href_with_retry(self.EXCEL)

    def back_to_jquery_href(self) -> str:
        self._hover(self.ENABLED, timeout=15)
        return self._get_href(self.BACK_TO_JQUERY, timeout=15)
