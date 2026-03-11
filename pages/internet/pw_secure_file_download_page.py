from __future__ import annotations

from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

from pages.core.pw_base_page import PWBasePage


class PWSecureFileDownloadPage(PWBasePage):
    URL_PATH = "/download_secure"

    FILE_LINKS = "#content a"
    HEADING = "h3"

    def open_with_credentials(
        self, username: str, password: str
    ) -> "PWSecureFileDownloadPage":
        base = self.config.base_url
        protocol, rest = base.split("://", maxsplit=1)
        auth_url = f"{protocol}://{username}:{password}@{rest}{self.URL_PATH}"
        self.page.goto(
            auth_url,
            wait_until="domcontentloaded",
            timeout=self.config.timeout_ms,
        )
        self.page.wait_for_selector(self.HEADING, timeout=self.config.timeout_ms)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

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

    def head_status_with_auth(
        self, url: str, username: str, password: str, timeout: int = 15
    ) -> int:
        try:
            response = requests.head(
                url,
                auth=HTTPBasicAuth(username, password),
                allow_redirects=True,
                timeout=timeout,
            )
            if response.status_code in (405, 501):
                raise RuntimeError("HEAD not supported")
            return response.status_code
        except Exception:
            response = requests.get(
                url,
                auth=HTTPBasicAuth(username, password),
                stream=True,
                allow_redirects=True,
                timeout=timeout,
            )
            try:
                return response.status_code
            finally:
                response.close()
