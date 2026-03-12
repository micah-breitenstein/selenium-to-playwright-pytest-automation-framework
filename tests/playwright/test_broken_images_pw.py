from __future__ import annotations

import pytest
import requests

from pages.internet import PWBrokenImagesPage


@pytest.mark.playwright
def test_broken_images_browser_detects_broken_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWBrokenImagesPage).open()
    broken_count = page.broken_image_count()
    assert broken_count >= 1, "Expected at least one broken image via naturalWidth"


@pytest.mark.playwright
def test_broken_images_api_status_codes_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWBrokenImagesPage).open()

    srcs = page.image_srcs()
    assert srcs, "No images found on the page"

    broken = []
    for url in srcs:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            broken.append((url, response.status_code))

    assert broken, "Expected at least one broken image, but all returned 200"
