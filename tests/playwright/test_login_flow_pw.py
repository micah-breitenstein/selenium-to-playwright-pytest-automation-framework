from __future__ import annotations

import pytest

from pages.internet import PWLoginPage


@pytest.mark.playwright
def test_login_failure_shows_error_playwright(pw_page_object_factory):
    login = pw_page_object_factory(PWLoginPage).load()
    login.login_expect_failure("baduser", "badpass")
    assert "Your username is invalid" in login.flash_message()
