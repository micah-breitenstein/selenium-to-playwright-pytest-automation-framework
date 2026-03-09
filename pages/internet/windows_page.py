from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.core.base_page import BasePage


class WindowsPage(BasePage):
    URL_PATH = "/windows"

    HEADING = (By.TAG_NAME, "h3")
    CLICK_HERE = (By.LINK_TEXT, "Click Here")

    def load(self) -> "WindowsPage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.HEADING)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def current_handle(self) -> str:
        return self.driver.current_window_handle

    def window_handles(self) -> list[str]:
        return list(self.driver.window_handles)

    def open_new_window(self, timeout: int = 10) -> str:
        existing = set(self.window_handles())
        self.click(self.CLICK_HERE)

        def has_new_window(drv):
            handles = set(drv.window_handles)
            new_handles = handles - existing
            return next(iter(new_handles)) if new_handles else False

        new_handle = WebDriverWait(self.driver, timeout).until(has_new_window)
        self.driver.switch_to.window(new_handle)
        self.wait_for_ready()
        return new_handle

    def switch_to_window(self, handle: str) -> None:
        self.driver.switch_to.window(handle)

    def close_current_window(self) -> None:
        self.driver.close()
