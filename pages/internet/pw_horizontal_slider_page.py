from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWHorizontalSliderPage(PWBasePage):
    URL_PATH = "/horizontal_slider"
    SLIDER = "input[type='range']"
    VALUE = "#range"

    def open(self) -> "PWHorizontalSliderPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.SLIDER)
        return self

    def value_text(self) -> str:
        text = self.locator(self.VALUE).text_content(timeout=self.config.timeout_ms)
        return (text or "").strip()

    def set_to(self, target: float) -> "PWHorizontalSliderPage":
        slider = self.locator(self.SLIDER)
        self.page.evaluate(
            """
            ([selector, value]) => {
                const el = document.querySelector(selector);
                el.value = String(value);
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
            """,
            [self.SLIDER, target],
        )
        self.locator(self.VALUE).filter(has_text=str(target)).wait_for(
            state="visible", timeout=self.config.timeout_ms
        )
        return self
