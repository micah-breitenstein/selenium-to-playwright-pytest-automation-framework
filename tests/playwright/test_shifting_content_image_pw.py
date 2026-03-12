from __future__ import annotations

import pytest

from pages.internet import PWShiftingContentImagePage


@pytest.mark.playwright
def test_shifting_content_image_default_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentImagePage).load()

    assert "/img/avatar.jpg" in page.image_src()
    assert page.current_url.endswith("/shifting_content/image")


@pytest.mark.playwright
def test_shifting_content_image_heading_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentImagePage).load()
    assert page.heading_text() == "Shifting Content: Image"


@pytest.mark.playwright
def test_shifting_content_image_random_mode_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentImagePage)
    page.go("/shifting_content/image?mode=random")
    page.expect_visible(page.IMAGE)

    assert "/img/avatar.jpg" in page.image_src()
    assert "mode=random" in page.current_url


@pytest.mark.playwright
def test_shifting_content_image_pixel_shift_mode_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWShiftingContentImagePage)
    page.go("/shifting_content/image?pixel_shift=100")
    page.expect_visible(page.IMAGE)

    assert "/img/avatar.jpg" in page.image_src()
    assert "pixel_shift=100" in page.current_url


@pytest.mark.playwright
def test_shifting_content_image_random_and_pixel_shift_mode_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWShiftingContentImagePage)
    page.go("/shifting_content/image?mode=random&pixel_shift=100")
    page.expect_visible(page.IMAGE)

    assert "/img/avatar.jpg" in page.image_src()
    current = page.current_url
    assert "mode=random" in current
    assert "pixel_shift=100" in current
