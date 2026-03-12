from __future__ import annotations

import pytest

from pages.internet import PWShiftingContentMenuPage

EXPECTED_MENU_ITEMS = ["Home", "About", "Contact Us", "Portfolio", "Gallery"]


@pytest.mark.playwright
def test_shifting_content_menu_items_default_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentMenuPage).load()

    assert page.menu_items() == EXPECTED_MENU_ITEMS
    assert page.current_url.endswith("/shifting_content/menu")


@pytest.mark.playwright
def test_shifting_content_menu_heading_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentMenuPage).load()
    assert page.heading_text() == "Shifting Content: Menu Element"


@pytest.mark.playwright
def test_shifting_content_menu_items_random_mode_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentMenuPage)
    page.go("/shifting_content/menu?mode=random")
    page.expect_visible(page.HEADING)

    assert page.menu_items() == EXPECTED_MENU_ITEMS
    assert "mode=random" in page.current_url


@pytest.mark.playwright
def test_shifting_content_menu_items_pixel_shift_mode_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWShiftingContentMenuPage)
    page.go("/shifting_content/menu?pixel_shift=100")
    page.expect_visible(page.HEADING)

    assert page.menu_items() == EXPECTED_MENU_ITEMS
    assert "pixel_shift=100" in page.current_url


@pytest.mark.playwright
def test_shifting_content_menu_items_random_and_pixel_shift_mode_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWShiftingContentMenuPage)
    page.go("/shifting_content/menu?mode=random&pixel_shift=100")
    page.expect_visible(page.HEADING)

    assert page.menu_items() == EXPECTED_MENU_ITEMS
    current = page.current_url
    assert "mode=random" in current
    assert "pixel_shift=100" in current
