from __future__ import annotations

import pytest

from pages.internet import PWShiftingContentImagePage


@pytest.mark.playwright
def test_shifting_content_image_default_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShiftingContentImagePage).load()

    assert "/img/avatar.jpg" in page.image_src()
    assert page.current_url.endswith("/shifting_content/image")
