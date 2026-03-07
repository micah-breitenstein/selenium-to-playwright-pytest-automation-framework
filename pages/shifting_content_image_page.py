from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class ShiftingContentImagePage(BasePage):
    URL_PATH = "/shifting_content/image"

    HEADING = (By.CSS_SELECTOR, "#content h3")
    IMAGE = (By.CSS_SELECTOR, "#content img")

    def load(self) -> "ShiftingContentImagePage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def load_random(self) -> "ShiftingContentImagePage":
        self.go(f"{self.URL_PATH}?mode=random")
        self.wait_for_ready()
        return self

    def load_with_pixel_shift(self, pixels: int) -> "ShiftingContentImagePage":
        self.go(f"{self.URL_PATH}?pixel_shift={pixels}")
        self.wait_for_ready()
        return self

    def load_random_with_pixel_shift(self, pixels: int) -> "ShiftingContentImagePage":
        self.go(f"{self.URL_PATH}?mode=random&pixel_shift={pixels}")
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.HEADING)
        self.wait_visible(self.IMAGE)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def image_src(self) -> str:
        return (self.find(self.IMAGE).get_attribute("src") or "").strip()

    def current_url(self) -> str:
        return self.driver.current_url
