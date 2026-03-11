from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWNestedFramesPage(PWBasePage):
    URL_PATH = "/nested_frames"

    def open(self) -> "PWNestedFramesPage":
        self.go(self.URL_PATH)
        self.page.wait_for_selector(
            "frame[name='frame-top']", timeout=self.config.timeout_ms
        )
        self.page.wait_for_selector(
            "frame[name='frame-bottom']", timeout=self.config.timeout_ms
        )
        return self

    def left_text(self) -> str:
        return (
            self.page.frame_locator("frame[name='frame-top']")
            .frame_locator("frame[name='frame-left']")
            .locator("body")
            .inner_text(timeout=self.config.timeout_ms)
            .strip()
        )

    def middle_text(self) -> str:
        return (
            self.page.frame_locator("frame[name='frame-top']")
            .frame_locator("frame[name='frame-middle']")
            .locator("#content")
            .inner_text(timeout=self.config.timeout_ms)
            .strip()
        )

    def right_text(self) -> str:
        return (
            self.page.frame_locator("frame[name='frame-top']")
            .frame_locator("frame[name='frame-right']")
            .locator("body")
            .inner_text(timeout=self.config.timeout_ms)
            .strip()
        )

    def bottom_text(self) -> str:
        return (
            self.page.frame_locator("frame[name='frame-bottom']")
            .locator("body")
            .inner_text(timeout=self.config.timeout_ms)
            .strip()
        )
