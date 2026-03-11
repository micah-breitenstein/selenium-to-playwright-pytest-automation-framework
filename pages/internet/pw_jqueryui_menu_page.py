from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWJQueryUIMenuPage(PWBasePage):
    URL_PATH = "/jqueryui/menu"

    MENU = "#menu"
    ENABLED = "#menu a:text-is('Enabled')"
    DOWNLOADS = "#menu a:text-is('Downloads')"
    PDF = "#menu a:text-is('PDF')"
    CSV = "#menu a:text-is('CSV')"
    EXCEL = "#menu a:text-is('Excel')"
    BACK_TO_JQUERY = "#menu a:text-is('Back to JQuery UI')"

    def open(self) -> "PWJQueryUIMenuPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.MENU)
        return self

    def open_downloads_menu(self) -> None:
        self.locator(self.ENABLED).hover(timeout=self.config.timeout_ms)
        self.locator(self.DOWNLOADS).hover(timeout=self.config.timeout_ms)
        self.page.wait_for_timeout(150)

    def _download_href(self, selector: str) -> str:
        self.open_downloads_menu()
        href = self.locator(selector).get_attribute("href", timeout=self.config.timeout_ms)
        if not href:
            raise AssertionError(f"No href found for selector: {selector}")
        return href

    def pdf_href(self) -> str:
        return self._download_href(self.PDF)

    def csv_href(self) -> str:
        return self._download_href(self.CSV)

    def excel_href(self) -> str:
        return self._download_href(self.EXCEL)

    def back_to_jquery_href(self) -> str:
        self.locator(self.ENABLED).hover(timeout=self.config.timeout_ms)
        href = self.locator(self.BACK_TO_JQUERY).get_attribute(
            "href", timeout=self.config.timeout_ms
        )
        if not href:
            raise AssertionError("No href found for Back to JQuery UI")
        return href
