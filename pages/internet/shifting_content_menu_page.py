from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class ShiftingContentMenuPage(BasePage):
    URL_PATH = "/shifting_content/menu"

    HEADING = (By.CSS_SELECTOR, "#content h3")
    MENU_LINKS = (By.CSS_SELECTOR, "#content ul li a")

    def load(self) -> "ShiftingContentMenuPage":
        self.go(self.URL_PATH)
        self.wait_for_ready()
        return self

    def load_random(self) -> "ShiftingContentMenuPage":
        self.go(f"{self.URL_PATH}?mode=random")
        self.wait_for_ready()
        return self

    def load_with_pixel_shift(self, pixels: int) -> "ShiftingContentMenuPage":
        self.go(f"{self.URL_PATH}?pixel_shift={pixels}")
        self.wait_for_ready()
        return self

    def load_random_with_pixel_shift(self, pixels: int) -> "ShiftingContentMenuPage":
        self.go(f"{self.URL_PATH}?mode=random&pixel_shift={pixels}")
        self.wait_for_ready()
        return self

    def wait_for_ready(self) -> None:
        self.wait_visible(self.HEADING)
        self.wait_visible(self.MENU_LINKS)

    def heading_text(self) -> str:
        return self.get_text(self.HEADING).strip()

    def current_url(self) -> str:
        return self.driver.current_url

    def menu_items(self) -> list[str]:
        links = self.find_all(self.MENU_LINKS)
        return [(link.text or "").strip() for link in links if (link.text or "").strip()]
