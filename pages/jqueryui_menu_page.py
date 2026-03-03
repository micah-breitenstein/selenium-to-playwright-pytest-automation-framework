from __future__ import annotations

from dataclasses import dataclass

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

    BACK_TO_JQUERY = (By.XPATH, "//*[@id='menu']//a[normalize-space()='Back to JQuery UI']")

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
        ActionChains(self.driver).move_to_element(el).pause(0.05).perform()

    def open_downloads_menu(self) -> None:
        self._hover(self.ENABLED, timeout=5)
        self._hover(self.DOWNLOADS, timeout=5)

    def _get_href(self, locator, timeout: float | None = None) -> str:
        el = self._visible(locator, timeout=timeout)
        href = el.get_attribute("href")
        if not href:
            raise AssertionError(f"No href attribute found for locator: {locator}")
        return href

    # ---- Public actions that return hrefs ----
    def pdf_href(self) -> str:
        self.open_downloads_menu()
        self._click(self.PDF, timeout=5)
        return self._get_href(self.PDF, timeout=5)

    def csv_href(self) -> str:
        self.open_downloads_menu()
        self._click(self.CSV, timeout=5)
        return self._get_href(self.CSV, timeout=5)

    def excel_href(self) -> str:
        self.open_downloads_menu()
        self._click(self.EXCEL, timeout=5)
        return self._get_href(self.EXCEL, timeout=5)

    def back_to_jquery_href(self) -> str:
        self._hover(self.ENABLED, timeout=5)
        return self._get_href(self.BACK_TO_JQUERY, timeout=5)