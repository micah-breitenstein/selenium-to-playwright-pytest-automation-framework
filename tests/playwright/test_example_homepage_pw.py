from __future__ import annotations

import pytest

from config.sites import SITES
from pages.example import PWHomePage


@pytest.mark.playwright
def test_homepage_heading_example_playwright(pw_page_object_factory):
    homepage = pw_page_object_factory(PWHomePage, base_url=SITES["example"])
    homepage.load()
    assert homepage.get_heading_text() == "Example Domain"
