from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class InfiniteScrollPage:
    URL_PATH = "/infinite_scroll"

    # jScroll appends items with this class (it’s what the demo uses)
    BLOCKS = (By.CSS_SELECTOR, ".jscroll-added")
    HEADER = (By.CSS_SELECTOR, "#content h3")  # "Infinite Scroll"

    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self) -> "InfiniteScrollPage":
        self.driver.get(self.base_url + self.URL_PATH)
        WebDriverWait(self.driver, 10).until(lambda d: d.find_element(*self.HEADER))
        return self

    def block_count(self) -> int:
        return len(self.driver.find_elements(*self.BLOCKS))

    def _scroll_height(self) -> int:
        return int(self.driver.execute_script("return document.body.scrollHeight;"))

    def _scroll_to_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def load_blocks(self, target_blocks: int = 3, timeout: int = 10, max_scrolls: int = 40) -> "InfiniteScrollPage":
        """
        Scroll until we have at least target_blocks blocks.
        Uses 2 signals to avoid flake:
          - block count increases OR
          - document height increases
        """
        wait = WebDriverWait(self.driver, timeout)

        for _ in range(max_scrolls):
            current_blocks = self.block_count()
            if current_blocks >= target_blocks:
                return self

            current_height = self._scroll_height()
            self._scroll_to_bottom()

            # Wait until either more blocks appear OR the page gets taller
            wait.until(
                lambda d: (
                    len(d.find_elements(*self.BLOCKS)) > current_blocks
                    or int(d.execute_script("return document.body.scrollHeight;")) > current_height
                )
            )

        raise AssertionError(
            f"Could not load {target_blocks} blocks after {max_scrolls} scrolls "
            f"(last block_count={self.block_count()}, scrollHeight={self._scroll_height()})"
        )