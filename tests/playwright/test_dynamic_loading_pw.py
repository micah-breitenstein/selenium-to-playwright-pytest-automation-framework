from __future__ import annotations

import pytest

from pages.internet import PWDynamicLoadingPage


@pytest.mark.playwright
def test_dynamic_loading_example_2_playwright(pw_page_object_factory):
    page = (
        pw_page_object_factory(PWDynamicLoadingPage)
        .open()
        .open_example_2()
        .start_loading()
    )

    assert "Hello World!" in page.finish_text()
