from __future__ import annotations

from urllib.parse import urljoin

from pages.core.pw_base_page import PWBasePage


class PWBrokenImagesPage(PWBasePage):
    URL_PATH = "/broken_images"
    IMAGES = "#content img"

    def open(self) -> "PWBrokenImagesPage":
        self.go(self.URL_PATH)
        self.locator(self.IMAGES).first.wait_for(
            state="attached", timeout=self.config.timeout_ms
        )
        return self

    def image_srcs(self) -> list[str]:
        srcs: list[str] = []
        for src in self.locator(self.IMAGES).evaluate_all(
            "elements => elements.map(e => e.getAttribute('src') || '')"
        ):
            value = src.strip()
            if not value:
                continue
            srcs.append(urljoin(self.config.base_url + "/", value))
        return srcs

    def broken_image_count(self) -> int:
        return int(
            self.locator(self.IMAGES).evaluate_all(
                "elements => elements.filter(e => e.complete && e.naturalWidth === 0).length"
            )
        )
