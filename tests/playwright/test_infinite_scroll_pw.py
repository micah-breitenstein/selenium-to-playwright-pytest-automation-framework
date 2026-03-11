from __future__ import annotations

import pytest

from pages.internet import PWInfiniteScrollPage


@pytest.mark.playwright
def test_infinite_scroll_loads_more_content_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWInfiniteScrollPage).open()
    page.load_blocks(target_blocks=15)
    assert page.block_count() >= 15
