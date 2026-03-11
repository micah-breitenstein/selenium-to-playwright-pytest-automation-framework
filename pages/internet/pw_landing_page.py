from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWLandingPage(PWBasePage):
    URL_PATH = "/"

    FORM_AUTH = "a:text-is('Form Authentication')"
    CHECKBOXES = "a:text-is('Checkboxes')"
    DROPDOWN = "a:text-is('Dropdown')"
    DYNAMIC_CONTROLS = "a:text-is('Dynamic Controls')"
    DYNAMIC_LOADING = "a:text-is('Dynamic Loading')"

    def load(self) -> "PWLandingPage":
        self.go(self.URL_PATH)
        return self

    def go_to_login(self) -> None:
        self.click(self.FORM_AUTH)

    def go_to_checkboxes(self) -> None:
        self.click(self.CHECKBOXES)

    def go_to_dropdown(self) -> None:
        self.click(self.DROPDOWN)

    def go_to_dynamic_controls(self) -> None:
        self.click(self.DYNAMIC_CONTROLS)

    def go_to_dynamic_loading(self) -> None:
        self.click(self.DYNAMIC_LOADING)
