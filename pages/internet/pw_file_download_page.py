from __future__ import annotations

from urllib.parse import urljoin

import requests

from pages.core.pw_base_page import PWBasePage


class PWFileDownloadPage(PWBasePage):
    URL_PATH = "/download"
    FILE_LINKS = "#content a"

    def open(self) -> "PWFileDownloadPage":
        self.go(self.URL_PATH)
        self.page.wait_for_selector(self.FILE_LINKS, timeout=self.config.timeout_ms)
        return self

    def file_hrefs(self) -> list[str]:
        hrefs: list[str] = []
        count = self.page.locator(self.FILE_LINKS).count()
        for index in range(count):
            href = (
                self.page.locator(self.FILE_LINKS)
                .nth(index)
                .get_attribute("href", timeout=self.config.timeout_ms)
            )
            if not href:
                continue
            hrefs.append(urljoin(self.config.base_url + "/", href.strip()))
        return hrefs

    def file_names(self) -> list[str]:
        names: list[str] = []
        count = self.page.locator(self.FILE_LINKS).count()
        for index in range(count):
            text = (
                self.page.locator(self.FILE_LINKS)
                .nth(index)
                .inner_text(timeout=self.config.timeout_ms)
                .strip()
            )
            if text:
                names.append(text)
        return names

    def head_status(self, url: str, timeout: int = 15) -> int:
        try:
            response = requests.head(url, allow_redirects=True, timeout=timeout)
            if response.status_code in (405, 501):
                raise RuntimeError("HEAD not supported")
            return response.status_code
        except Exception:
            response = requests.get(url, stream=True, allow_redirects=True, timeout=timeout)
            try:
                return response.status_code
            finally:
                response.close()
