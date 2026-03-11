from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWTyposPage(PWBasePage):
    URL_PATH = "/typos"
    HEADING = "h3"
    CONTENT = "#content"

    def open(self) -> "PWTyposPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def content_text(self) -> str:
        return self.get_text(self.CONTENT)

    def has_expected_typos_sentence(self) -> bool:
        text = self.content_text()
        return (
            "Sometimes you'll see a typo, other times you won't." in text
            or "Sometimes you'll see a typo, other times you won,t." in text
        )
