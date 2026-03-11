from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWHoversPage(PWBasePage):
    URL_PATH = "/hovers"
    FIGURES = ".figure"

    def open(self) -> "PWHoversPage":
        self.go(self.URL_PATH)
        self.locator(self.FIGURES).first.wait_for(
            state="visible", timeout=self.config.timeout_ms
        )
        return self

    def _figure(self, user_index_1_based: int):
        return self.locator(self.FIGURES).nth(user_index_1_based - 1)

    def hover_user(self, user_index_1_based: int) -> "PWHoversPage":
        figure = self._figure(user_index_1_based)
        figure.hover(timeout=self.config.timeout_ms)
        figure.locator(".figcaption").wait_for(
            state="visible", timeout=self.config.timeout_ms
        )
        return self

    def user_name_text(self, user_index_1_based: int) -> str:
        text = (
            self._figure(user_index_1_based)
            .locator(".figcaption h5")
            .text_content(timeout=self.config.timeout_ms)
        )
        return (text or "").strip()

    def user_profile_href(self, user_index_1_based: int) -> str:
        href = (
            self._figure(user_index_1_based)
            .locator(".figcaption a")
            .get_attribute("href", timeout=self.config.timeout_ms)
        )
        return href or ""
