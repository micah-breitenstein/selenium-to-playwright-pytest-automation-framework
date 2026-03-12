from __future__ import annotations

import pytest

from pages.internet import PWLoginPage


@pytest.mark.playwright
def test_login_success_playwright(pw_page_object_factory):
    secure = (
        pw_page_object_factory(PWLoginPage)
        .load()
        .login("tomsmith", "SuperSecretPassword!")
    )

    assert "Secure Area" in secure.header()
    assert "You logged into a secure area" in secure.flash_message()


@pytest.mark.playwright
def test_login_failure_shows_error_playwright(pw_page_object_factory):
    login = pw_page_object_factory(PWLoginPage).load()
    login.login_expect_failure("baduser", "badpass")
    assert "Your username is invalid" in login.flash_message()
