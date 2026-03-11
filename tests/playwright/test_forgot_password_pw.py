from __future__ import annotations

import pytest

from pages.internet import PWForgotPasswordPage


@pytest.mark.playwright
def test_forgot_password_submit_shows_known_outcome_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWForgotPasswordPage).open()
    result = page.retrieve_password("micah@example.com")

    assert result.is_internal_server_error() or result.is_success_message(), (
        "Unexpected forgot password result page.\n\n"
        f"Body text was:\n{result.body_text()}"
    )
