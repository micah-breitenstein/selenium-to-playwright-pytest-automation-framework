from __future__ import annotations

import logging
from dataclasses import dataclass
from urllib.parse import urljoin

from playwright.sync_api import Locator, Page, expect


@dataclass(frozen=True)
class PWConfig:
    base_url: str
    timeout_ms: int = 60_000


class PWBasePage:
    def __init__(
        self,
        page: Page,
        config: PWConfig | None = None,
        *,
        base_url: str | None = None,
        timeout_ms: int = 60_000,
    ) -> None:
        self.page = page
        self.log = logging.getLogger(self.__class__.__name__)

        if config is None:
            if base_url is None:
                base_url = "https://the-internet.herokuapp.com"
            config = PWConfig(base_url=base_url.rstrip("/"), timeout_ms=timeout_ms)
        else:
            if base_url is not None:
                config = PWConfig(
                    base_url=base_url.rstrip("/"), timeout_ms=config.timeout_ms
                )

        self.config = config

    def go(self, path: str) -> None:
        url = urljoin(self.config.base_url + "/", path.lstrip("/"))
        self.log.info(f"BASE_URL = {self.config.base_url}")
        self.log.info(f"GO → {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.config.timeout_ms)

    @property
    def current_url(self) -> str:
        return self.page.url

    @property
    def page_title(self) -> str:
        return self.page.title()

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def click(self, selector: str) -> None:
        self.log.info(f"CLICK → {selector}")
        self.page.locator(selector).click(timeout=self.config.timeout_ms)

    def fill(self, selector: str, text: str) -> None:
        redacted = "***" if "password" in selector.lower() else text
        self.log.info(f"FILL → {selector} value={redacted!r}")
        self.page.locator(selector).fill(text, timeout=self.config.timeout_ms)

    def get_text(self, selector: str) -> str:
        self.log.info(f"GET_TEXT → {selector}")
        text = self.page.locator(selector).inner_text(timeout=self.config.timeout_ms)
        return text.strip()

    def expect_visible(self, selector: str) -> None:
        self.log.info(f"EXPECT visible → {selector}")
        expect(self.page.locator(selector)).to_be_visible(timeout=self.config.timeout_ms)
