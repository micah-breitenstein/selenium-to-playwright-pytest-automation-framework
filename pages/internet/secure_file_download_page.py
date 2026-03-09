from __future__ import annotations

from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SecureFileDownloadPage:
    URL_PATH = "/download_secure"

    FILE_LINKS = (By.CSS_SELECTOR, "#content a")
    HEADING = (By.TAG_NAME, "h3")

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open_with_credentials(self, username: str, password: str) -> "SecureFileDownloadPage":
        """Open the page with basic auth credentials embedded in URL."""
        protocol, rest = self.base_url.split("://")
        auth_url = f"{protocol}://{username}:{password}@{rest}{self.URL_PATH}"
        self.driver.get(auth_url)
        self.wait.until(EC.presence_of_element_located(self.HEADING))
        return self

    def heading_text(self) -> str:
        el = self.wait.until(EC.visibility_of_element_located(self.HEADING))
        return el.text.strip()

    def file_names(self) -> list[str]:
        links = self.driver.find_elements(*self.FILE_LINKS)
        return [(a.text or "").strip() for a in links if (a.text or "").strip()]

    def file_hrefs(self) -> list[str]:
        """Return absolute URLs for each download link on the page."""
        links = self.driver.find_elements(*self.FILE_LINKS)
        hrefs: list[str] = []
        for a in links:
            href = (a.get_attribute("href") or "").strip()
            if not href:
                continue
            hrefs.append(urljoin(self.base_url + "/", href))
        return hrefs

    def head_status_with_auth(
        self, url: str, username: str, password: str, timeout: int = 15
    ) -> int:
        """Check file status with basic auth credentials."""
        try:
            r = requests.head(
                url,
                auth=HTTPBasicAuth(username, password),
                allow_redirects=True,
                timeout=timeout,
            )
            if r.status_code in (405, 501):
                raise RuntimeError("HEAD not supported")
            return r.status_code
        except Exception:
            r = requests.get(
                url,
                auth=HTTPBasicAuth(username, password),
                stream=True,
                allow_redirects=True,
                timeout=timeout,
            )
            try:
                return r.status_code
            finally:
                r.close()
