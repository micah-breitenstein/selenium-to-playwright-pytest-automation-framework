from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWForgotPasswordPage(PWBasePage):
    URL_PATH = "/forgot_password"
    EMAIL_INPUT = "#email"
    RETRIEVE_BUTTON = "#form_submit"

    def open(self) -> "PWForgotPasswordPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.EMAIL_INPUT)
        return self

    def set_email(self, email: str) -> "PWForgotPasswordPage":
        self.fill(self.EMAIL_INPUT, email)
        return self

    def submit(self) -> "PWForgotPasswordResultPage":
        self.click(self.RETRIEVE_BUTTON)
        self.page.wait_for_load_state(
            "domcontentloaded", timeout=self.config.timeout_ms
        )
        return PWForgotPasswordResultPage(self.page)

    def retrieve_password(self, email: str) -> "PWForgotPasswordResultPage":
        return self.set_email(email).submit()


class PWForgotPasswordResultPage:
    def __init__(self, page) -> None:
        self.page = page

    def body_text(self) -> str:
        return (self.page.locator("body").inner_text() or "").strip()

    def is_internal_server_error(self) -> bool:
        return "Internal Server Error" in self.body_text()

    def is_success_message(self) -> bool:
        text = self.body_text()
        return "Your e-mail's been sent!" in text or "Your e-mail’s been sent!" in text
