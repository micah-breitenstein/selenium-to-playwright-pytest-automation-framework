from __future__ import annotations

import pytest

from pages.internet import PWHoversPage


@pytest.mark.playwright
def test_hover_reveals_user1_name_and_link_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWHoversPage).open()

    page.hover_user(1)

    assert page.user_name_text(1) == "name: user1"
    assert page.user_profile_href(1).endswith("/users/1")


@pytest.mark.playwright
def test_click_view_profile_navigates_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWHoversPage).open()

    page.hover_user(2)
    page.page.locator(".figure").nth(1).locator(".figcaption a").click(
        timeout=page.config.timeout_ms
    )

    assert page.current_url.endswith("/users/2")
