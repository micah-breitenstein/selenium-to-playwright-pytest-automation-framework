from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWWindowsPage(PWBasePage):
    URL_PATH = "/windows"
    HEADING = "h3"
    CLICK_HERE = "text=Click Here"

    def load(self) -> "PWWindowsPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.HEADING)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def open_new_window(self) -> None:
        with self.page.context.expect_page() as new_page_info:
            self.click(self.CLICK_HERE)
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded", timeout=self.config.timeout_ms)
        self.page = new_page

    def close_current_window(self) -> None:
        self.page.close()

    def switch_to_first_window(self) -> None:
        first = self.page.context.pages[0]
        first.bring_to_front()
        self.page = first
