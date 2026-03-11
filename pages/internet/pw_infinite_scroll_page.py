from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWInfiniteScrollPage(PWBasePage):
    URL_PATH = "/infinite_scroll"
    BLOCKS = ".jscroll-added"
    HEADER = "#content h3"

    def open(self) -> "PWInfiniteScrollPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADER)
        return self

    def block_count(self) -> int:
        return self.locator(self.BLOCKS).count()

    def _scroll_height(self) -> int:
        return int(self.page.evaluate("document.body.scrollHeight"))

    def _scroll_to_bottom(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def load_blocks(self, target_blocks: int = 3, max_scrolls: int = 40) -> "PWInfiniteScrollPage":
        for _ in range(max_scrolls):
            current_blocks = self.block_count()
            if current_blocks >= target_blocks:
                return self

            current_height = self._scroll_height()
            self._scroll_to_bottom()
            self.page.wait_for_function(
                "([selector, blocks, height]) => document.querySelectorAll(selector).length > blocks || document.body.scrollHeight > height",
                arg=[self.BLOCKS, current_blocks, current_height],
                timeout=self.config.timeout_ms,
            )

        raise AssertionError(
            f"Could not load {target_blocks} blocks after {max_scrolls} scrolls "
            f"(last block_count={self.block_count()}, scrollHeight={self._scroll_height()})"
        )
