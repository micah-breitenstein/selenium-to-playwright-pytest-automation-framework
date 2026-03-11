from __future__ import annotations

import pytest

from pages.internet import PWLoginPage


@pytest.mark.playwright
def test_login_success_reaches_secure_area_playwright(pw_page_object_factory):
    secure = pw_page_object_factory(PWLoginPage).load().login(
        "tomsmith", "SuperSecretPassword!"
    )

    assert "Secure Area" in secure.header()
    assert "You logged into a secure area" in secure.flash_message()
