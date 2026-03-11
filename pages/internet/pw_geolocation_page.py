from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWGeolocationPage(PWBasePage):
    URL_PATH = "/geolocation"
    BTN = "#content button"
    LAT = "#lat-value"
    LONG = "#long-value"

    def open(self) -> "PWGeolocationPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.BTN)
        return self

    def click_where_am_i(self) -> "PWGeolocationPage":
        self.click(self.BTN)
        return self

    def wait_for_coordinates(self) -> "PWGeolocationPage":
        self.page.wait_for_function(
            "([lat, lon]) => {"
            " const latText = (document.querySelector(lat)?.textContent || '').trim();"
            " const lonText = (document.querySelector(lon)?.textContent || '').trim();"
            " return latText !== '' && lonText !== '';"
            "}",
            arg=[self.LAT, self.LONG],
            timeout=self.config.timeout_ms,
        )
        return self

    def lat_text(self) -> str:
        return self.get_text(self.LAT)

    def long_text(self) -> str:
        return self.get_text(self.LONG)
