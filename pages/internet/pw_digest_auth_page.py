from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWDigestAuthPage(PWBasePage):
    URL_PATH = "/digest_auth"

    def open_with_credentials(
        self,
        username: str = "admin",
        password: str = "admin",
    ) -> "PWDigestAuthPage":
        base = self.config.base_url
        protocol, rest = base.split("://", maxsplit=1)
        auth_url = f"{protocol}://{username}:{password}@{rest}{self.URL_PATH}"
        self.page.goto(
            auth_url,
            wait_until="domcontentloaded",
            timeout=self.config.timeout_ms,
        )
        return self
