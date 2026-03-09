from __future__ import annotations

from dataclasses import dataclass

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class EntryAdPage:
    driver: WebDriver
    base_url: str
    timeout: float = 10.0
    check_timeout: float = 1.0

    PATH = "/entry_ad"

    # -------------------------
    # Locators
    # -------------------------

    MODAL = (By.ID, "modal")  # overlay/container (may remain present)
    MODAL_CONTENT = (By.CSS_SELECTOR, "#modal .modal")  # dialog box
    MODAL_TITLE = (By.CSS_SELECTOR, "#modal .modal-title h3")
    MODAL_CLOSE = (By.CSS_SELECTOR, "#modal .modal-footer p")  # "Close" <p> in demo

    RESTART_AD = (By.ID, "restart-ad")
    RESTART_AD_FALLBACK = (By.LINK_TEXT, "click here")

    # -------------------------
    # Navigation
    # -------------------------

    def url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.PATH}"

    def open(self) -> "EntryAdPage":
        self.driver.get(self.url())
        return self

    # -------------------------
    # Modal helpers
    # -------------------------

    def modal_is_visible(self, timeout: float = 2.0) -> bool:
        """Fast probe: is the *dialog* visible?"""
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.visibility_of_element_located(self.MODAL_CONTENT))
            return True
        except TimeoutException:
            return False

    def wait_for_modal(self, timeout: float = 10.0) -> "EntryAdPage":
        """
        Purposeful wait — used when we EXPECT the modal to appear.
        Waits until dialog is visible AND title text is present.
        """
        wait = WebDriverWait(self.driver, timeout)

        def ready(d: WebDriver):
            try:
                dialog = d.find_element(*self.MODAL_CONTENT)
                if not dialog.is_displayed():
                    return False
                title = d.find_element(*self.MODAL_TITLE).text.strip()
                return title if title else False
            except StaleElementReferenceException:
                return False
            except Exception:
                return False

        wait.until(ready)
        return self

    def modal_title(self, timeout: float = 3.0) -> str:
        """Return modal title, waiting briefly until it is non-empty."""
        wait = WebDriverWait(self.driver, timeout)

        def title_has_text(d: WebDriver):
            try:
                el = d.find_element(*self.MODAL_TITLE)
                text = (el.text or "").strip()
                return text if text else False
            except StaleElementReferenceException:
                return False

        try:
            return str(wait.until(title_has_text)).strip()
        except TimeoutException:
            return ""

    def close_modal(self, timeout: float = 5.0) -> "EntryAdPage":
        """
        Click Close and wait until the dialog disappears.
        Note: the overlay container may remain; we only care that the dialog is gone.
        """
        wait = WebDriverWait(self.driver, timeout)

        # Ensure the dialog is visible before trying to close
        wait.until(EC.visibility_of_element_located(self.MODAL_CONTENT))

        # Click the Close control
        try:
            wait.until(EC.element_to_be_clickable(self.MODAL_CLOSE)).click()
        except (
            TimeoutException,
            ElementClickInterceptedException,
            StaleElementReferenceException,
        ):
            el = self.driver.find_element(*self.MODAL_CLOSE)
            self.driver.execute_script("arguments[0].click();", el)

        # Wait until dialog is not visible
        try:
            wait.until(EC.invisibility_of_element_located(self.MODAL_CONTENT))
        except TimeoutException:
            # If it never transitions cleanly, don't hard-fail here; tests can decide
            pass

        return self

    # -------------------------
    # Restart Ad
    # -------------------------

    def restart_ad(self, timeout: float = 5.0) -> "EntryAdPage":
        """
        Clicks restart ad link.
        Does NOT assume modal appears instantly — call wait_for_modal() after.
        """
        wait = WebDriverWait(self.driver, timeout)

        try:
            link = wait.until(EC.element_to_be_clickable(self.RESTART_AD))
        except TimeoutException:
            link = wait.until(EC.element_to_be_clickable(self.RESTART_AD_FALLBACK))

        try:
            link.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", link)

        return self
