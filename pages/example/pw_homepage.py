from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWHomePage(PWBasePage):
    HEADING = "h1"

    def load(self) -> "PWHomePage":
        self.go("/")
        return self

    def get_heading_text(self) -> str:
        return self.get_text(self.HEADING)
