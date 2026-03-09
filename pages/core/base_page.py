from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Type alias for Selenium locator tuples, e.g. (By.ID, "username")
Locator = tuple[str, str]


@dataclass(frozen=True)
class Config:
    base_url: str
    timeout: int = 10


class BasePage:
    def __init__(
        self,
        driver: WebDriver,
        config: Config | None = None,
        *,
        base_url: str | None = None,
        timeout: int = 10,
    ) -> None:
        """
        Supports:
            BasePage(driver, base_url="http://127.0.0.1:9292")
            BasePage(driver, config=Config(...))
        """

        self.driver: WebDriver = driver
        self.log = logging.getLogger(self.__class__.__name__)

        # Build config safely at runtime (never as default argument)
        if config is None:
            if base_url is None:
                # Fallback default (safe)
                base_url = "https://the-internet.herokuapp.com"
            config = Config(base_url=base_url.rstrip("/"), timeout=timeout)
        else:
            # Allow explicit base_url override even if config passed
            if base_url is not None:
                config = Config(
                    base_url=base_url.rstrip("/"),
                    timeout=config.timeout,
                )

        self.config = config
        self.wait = WebDriverWait(driver, self.config.timeout)

    # -------------------------
    # Navigation
    # -------------------------
    def go(self, path: str) -> None:
        url = urljoin(self.config.base_url + "/", path.lstrip("/"))
        self.log.info(f"BASE_URL = {self.config.base_url}")
        self.log.info(f"GO → {url}")
        self.driver.get(url)

    # -------------------------
    # Properties
    # -------------------------
    @property
    def current_url(self) -> str:
        """Return the browser's current URL."""
        return self.driver.current_url

    @property
    def page_title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    # -------------------------
    # Wait Helpers
    # -------------------------
    def wait_visible(self, locator: Locator) -> WebElement:
        self.log.info(f"WAIT visible → {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator: Locator) -> WebElement:
        self.log.info(f"WAIT clickable → {locator}")
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator: Locator) -> bool:
        self.log.info(f"WAIT invisible → {locator}")
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_present(self, locator: Locator) -> WebElement:
        """Wait for element in DOM (not necessarily visible)."""
        self.log.info(f"WAIT present → {locator}")
        return self.wait.until(EC.presence_of_element_located(locator))

    # -------------------------
    # Actions
    # -------------------------
    def click(self, locator: Locator) -> None:
        self.log.info(f"CLICK → {locator}")
        self.wait_clickable(locator).click()

    def type(self, locator: Locator, text: str, clear: bool = True) -> None:
        # Redact likely passwords
        redacted = "***" if "password" in str(locator).lower() else text
        self.log.info(f"TYPE → {locator} value={redacted!r} clear={clear}")

        el = self.wait_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def get_text(self, locator: Locator) -> str:
        self.log.info(f"GET_TEXT → {locator}")
        return self.wait_visible(locator).text

    def is_visible(self, locator: Locator, timeout: int = 1) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.log.info(f"VISIBLE ✓ {locator}")
            return True
        except Exception:
            self.log.info(f"NOT VISIBLE ✗ {locator}")
            return False

    def wait_any(
        self, locator_a: Locator, locator_b: Locator, timeout: int = 10
    ) -> str:
        """
        Wait until either locator_a or locator_b is visible.
        Returns "first" if locator_a wins, "second" if locator_b wins.
        """
        self.log.info(f"WAIT_ANY → {locator_a} OR {locator_b} timeout={timeout}s")

        end = time.time() + timeout
        while time.time() < end:
            if self.is_visible(locator_a, timeout=0.2):
                self.log.info("WAIT_ANY result → first")
                return "first"
            if self.is_visible(locator_b, timeout=0.2):
                self.log.info("WAIT_ANY result → second")
                return "second"

        self.log.error("WAIT_ANY timed out")
        raise TimeoutError(f"Neither locator became visible within {timeout}s")

    def find(self, locator: Locator) -> WebElement:
        self.log.info(f"FIND → {locator}")
        return self.driver.find_element(*locator)

    def find_all(self, locator: Locator) -> list[WebElement]:
        self.log.info(f"FIND ALL → {locator}")
        return self.driver.find_elements(*locator)

    # -------------------------
    # JavaScript
    # -------------------------
    def js_execute(self, script: str, *args: Any) -> Any:
        """Execute JavaScript in the browser and return the result."""
        self.log.info(f"JS → {script[:80]}{'…' if len(script) > 80 else ''}")
        return self.driver.execute_script(script, *args)

    # -------------------------
    # Scrolling
    # -------------------------
    def scroll_to(self, locator: Locator) -> WebElement:
        """Scroll an element into view using JavaScript."""
        el = self.wait_present(locator)
        self.log.info(f"SCROLL_TO → {locator}")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", el
        )
        return el

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        self.log.info("SCROLL → bottom")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # -------------------------
    # Debugging
    # -------------------------
    def highlight(
        self, locator: Locator, color: str = "red", duration: float = 0.5
    ) -> WebElement:
        """Briefly highlight an element with a colored border for visual debugging."""
        el = self.wait_visible(locator)
        original = el.value_of_css_property("border")
        self.driver.execute_script(
            "arguments[0].style.border = arguments[1];", el, f"3px solid {color}"
        )
        if duration:
            import time

            time.sleep(duration)
            self.driver.execute_script(
                "arguments[0].style.border = arguments[1];", el, original
            )
        self.log.info(f"HIGHLIGHT → {locator} color={color}")
        return el

    # -------------------------
    # Text Helpers
    # -------------------------
    def wait_for_text(self, locator, expected: str, timeout: int | None = None) -> bool:
        """Wait until the element's text contains *expected*."""
        t = timeout or self.config.timeout
        self.log.info(f"WAIT_TEXT → {locator} contains {expected!r} timeout={t}s")
        return WebDriverWait(self.driver, t).until(
            EC.text_to_be_present_in_element(locator, expected)
        )

    def get_attribute(self, locator: Locator, attr: str) -> str | None:
        """Return an attribute value from the first matching element."""
        el = self.wait_present(locator)
        value = el.get_attribute(attr)
        self.log.info(f"GET_ATTR → {locator} {attr}={value!r}")
        return value

    # -------------------------
    # Dropdown / Select
    # -------------------------
    def select_by_value(self, locator: Locator, value: str) -> None:
        """Select an <option> by its ``value`` attribute."""
        from selenium.webdriver.support.ui import Select

        el = self.wait_visible(locator)
        Select(el).select_by_value(value)
        self.log.info(f"SELECT value={value!r} → {locator}")

    def select_by_text(self, locator: Locator, text: str) -> None:
        """Select an <option> by its visible text."""
        from selenium.webdriver.support.ui import Select

        el = self.wait_visible(locator)
        Select(el).select_by_visible_text(text)
        self.log.info(f"SELECT text={text!r} → {locator}")

    def selected_option_text(self, locator: Locator) -> str:
        """Return the visible text of the currently selected <option>."""
        from selenium.webdriver.support.ui import Select

        el = self.wait_visible(locator)
        text = Select(el).first_selected_option.text
        self.log.info(f"SELECTED text={text!r} ← {locator}")
        return text

    # -------------------------
    # Frames / iframes
    # -------------------------
    def switch_to_frame(self, locator: Locator) -> None:
        """Switch into an iframe identified by *locator*."""
        el = self.wait_present(locator)
        self.driver.switch_to.frame(el)
        self.log.info(f"FRAME → {locator}")

    def switch_to_default(self) -> None:
        """Switch back to the top-level document."""
        self.driver.switch_to.default_content()
        self.log.info("FRAME → default")
