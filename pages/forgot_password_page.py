from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


@dataclass
class ForgotPasswordPage:
    driver: WebDriver
    base_url: str

    PATH = "/forgot_password"

    # Locators
    EMAIL_INPUT = (By.ID, "email")
    RETRIEVE_BUTTON = (By.ID, "form_submit")
    FORM = (By.ID, "forgot_password")

    def url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.PATH}"

    def open(self) -> "ForgotPasswordPage":
        self.driver.get(self.url())
        self.wait_for_loaded()
        return self

    def wait_for_loaded(self, timeout: int = 10) -> None:
        """
        Parallel-safe readiness:
        - Prefer presence over visibility (visibility can be flaky under load)
        - Fallback to form/body checks to avoid false timeouts
        """
        wait = WebDriverWait(self.driver, timeout)

        def ready(d: WebDriver):
            try:
                # If the input is present, we're good (even if not "visible" yet)
                d.find_element(*self.EMAIL_INPUT)
                return True
            except Exception:
                pass

            # Fallback: form exists or page text indicates we're on the right page
            try:
                d.find_element(*self.FORM)
                return True
            except Exception:
                pass

            try:
                body = d.find_element(By.TAG_NAME, "body").text
                return "Forgot Password" in body
            except Exception:
                return False

        wait.until(ready)

    def set_email(self, email: str) -> "ForgotPasswordPage":
        el = self.driver.find_element(*self.EMAIL_INPUT)
        el.clear()
        el.send_keys(email)
        return self

    def submit(self) -> "ForgotPasswordResultPage":
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.element_to_be_clickable(self.RETRIEVE_BUTTON))

        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

        # Wait for a meaningful change:
        # - URL changes
        # - OR email input disappears
        # - OR known outcome text appears
        def changed(d: WebDriver):
            try:
                url_changed = (self.PATH not in d.current_url)

                try:
                    body_text = d.find_element(By.TAG_NAME, "body").text
                except StaleElementReferenceException:
                    return False

                has_outcome_text = (
                    "Internal Server Error" in body_text
                    or "Your e-mail" in body_text
                    or "Your e-mail's been sent!" in body_text
                    or "Your e-mail’s been sent!" in body_text
                )

                try:
                    d.find_element(*self.EMAIL_INPUT)
                    email_still_there = True
                except Exception:
                    email_still_there = False

                return url_changed or has_outcome_text or (not email_still_there)

            except StaleElementReferenceException:
                return False

        try:
            wait.until(changed)
        except TimeoutException:
            # Don't fail the page object; let the test assert on the result wrapper.
            pass

        return ForgotPasswordResultPage(self.driver)

    def retrieve_password(self, email: str) -> "ForgotPasswordResultPage":
        return self.set_email(email).submit()


class ForgotPasswordResultPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def body_text(self) -> str:
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except StaleElementReferenceException:
            # one retry
            return self.driver.find_element(By.TAG_NAME, "body").text

    def is_internal_server_error(self) -> bool:
        return "Internal Server Error" in self.body_text()

    def is_success_message(self) -> bool:
        text = self.body_text()
        return "Your e-mail's been sent!" in text or "Your e-mail’s been sent!" in text