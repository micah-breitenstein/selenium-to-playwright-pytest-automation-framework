from __future__ import annotations

import pytest

from pages.internet import PWBrokenImagesPage


@pytest.mark.playwright
def test_broken_images_browser_detects_broken_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWBrokenImagesPage).open()
    broken_count = page.broken_image_count()
    assert broken_count >= 1, "Expected at least one broken image via naturalWidth"
