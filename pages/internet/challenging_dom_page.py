from __future__ import annotations

import hashlib
from dataclasses import dataclass

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class ChallengingDomPage:
    driver: WebDriver
    base_url: str
    timeout: int = 10

    URL_PATH = "/challenging_dom"

    TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")

    BLUE_BTN = (By.CSS_SELECTOR, "a.button:not(.alert):not(.success)")
    RED_BTN = (By.CSS_SELECTOR, "a.button.alert")
    GREEN_BTN = (By.CSS_SELECTOR, "a.button.success")
    ALL_BTNS = (By.CSS_SELECTOR, "#content a.button")

    CANVAS = (By.CSS_SELECTOR, "canvas")  # the <canvas> element (no id on page)

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        self.wait = WebDriverWait(self.driver, self.timeout)

    # -------------------------
    # Navigation / readiness
    # -------------------------

    def open(self) -> None:
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        self.wait_for_ready()

    def wait_for_ready(self, timeout: int | None = None) -> None:
        t = timeout if timeout is not None else self.timeout
        w = WebDriverWait(self.driver, t)
        # canvas + buttons + at least one row
        w.until(EC.presence_of_element_located(self.CANVAS))
        w.until(EC.presence_of_all_elements_located(self.ALL_BTNS))
        w.until(EC.presence_of_all_elements_located(self.TABLE_ROWS))

    def current_url(self) -> str:
        return self.driver.current_url

    # -------------------------
    # Canvas fingerprinting
    # -------------------------

    def canvas_data_url(self) -> str:
        """
        Always re-find the canvas element (never hold a stale WebElement).
        """
        try:
            canvas = self.driver.find_element(*self.CANVAS)
            return self.driver.execute_script(
                "return arguments[0].toDataURL('image/png');", canvas
            )
        except StaleElementReferenceException:
            # one immediate retry
            canvas = self.driver.find_element(*self.CANVAS)
            return self.driver.execute_script(
                "return arguments[0].toDataURL('image/png');", canvas
            )

    def answer_value(self) -> str:
        data_url = self.canvas_data_url()
        if not data_url:
            return ""
        return hashlib.sha256(data_url.encode("utf-8")).hexdigest()

    def wait_for_canvas_change(self, before: str, timeout: int = 5) -> str:
        wait = WebDriverWait(self.driver, timeout)

        def changed(d):
            try:
                after = self.canvas_data_url()
                return after if after and after != before else False
            except StaleElementReferenceException:
                return False

        return wait.until(changed)

    def wait_for_answer_to_change(self, before: str, timeout: int = 5) -> str:
        wait = WebDriverWait(self.driver, timeout)

        def changed(d):
            try:
                after = self.answer_value()
                return after if after and after != before else False
            except StaleElementReferenceException:
                return False

        return wait.until(changed)

    # -------------------------
    # Buttons
    # -------------------------

    def button_texts(self) -> dict[str, str]:
        """
        Read button labels; tolerate transient staleness during redraw.
        """
        try:
            return {
                "blue": self.driver.find_element(*self.BLUE_BTN).text.strip(),
                "red": self.driver.find_element(*self.RED_BTN).text.strip(),
                "green": self.driver.find_element(*self.GREEN_BTN).text.strip(),
            }
        except StaleElementReferenceException:
            return {
                "blue": self.driver.find_element(*self.BLUE_BTN).text.strip(),
                "red": self.driver.find_element(*self.RED_BTN).text.strip(),
                "green": self.driver.find_element(*self.GREEN_BTN).text.strip(),
            }

    def click_button(self, color: str, timeout: int = 5) -> None:
        mapping = {"blue": self.BLUE_BTN, "red": self.RED_BTN, "green": self.GREEN_BTN}
        try:
            locator = mapping[color.lower().strip()]
        except KeyError:
            raise ValueError("color must be one of: blue, red, green")

        w = WebDriverWait(self.driver, timeout)
        el = w.until(EC.element_to_be_clickable(locator))

        # Click with fallback (parallel load can cause intercepts)
        try:
            el.click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            el = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", el)

    def wait_for_button_texts_to_change(
        self, before: dict[str, str], timeout: int = 5
    ) -> dict[str, str]:
        """
        The demo sometimes redraws quickly; during the redraw, elements can go stale.
        This wait re-reads labels and treats stale as "not ready yet".
        """
        wait = WebDriverWait(self.driver, timeout)

        def changed(d):
            try:
                after = self.button_texts()
                return after if after != before else False
            except StaleElementReferenceException:
                return False

        return wait.until(changed)

    # -------------------------
    # Table rows / delete action
    # -------------------------

    def rows(self):
        return self.driver.find_elements(*self.TABLE_ROWS)

    def click_delete_by_column_text(
        self, column_index: int, expected_text: str
    ) -> None:
        """
        column_index is 0-based
        Retry once if the table redraws mid-iteration (stale row).
        """
        attempts = 2
        last_err: Exception | None = None

        for _ in range(attempts):
            try:
                for row in self.rows():
                    try:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if column_index >= len(cells):
                            continue

                        cell_text = cells[column_index].text.strip()
                        if expected_text in cell_text:
                            # "delete" link exists in the row
                            link = row.find_element(By.LINK_TEXT, "delete")
                            try:
                                link.click()
                            except (
                                ElementClickInterceptedException,
                                StaleElementReferenceException,
                            ):
                                self.driver.execute_script(
                                    "arguments[0].click();", link
                                )
                            return
                    except StaleElementReferenceException:
                        # row went stale during redraw; break to outer retry
                        raise

                # no match found (stable)
                break

            except (StaleElementReferenceException, NoSuchElementException) as e:
                last_err = e
                self.wait_for_ready(timeout=5)

        raise AssertionError(
            f"No row found where column {column_index} contains '{expected_text}'"
        ) from last_err
