from __future__ import annotations

import pytest

from pages.internet import PWHorizontalSliderPage


@pytest.mark.playwright
def test_horizontal_slider_can_set_value_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWHorizontalSliderPage).open()

    page.set_to(3.5)

    assert page.value_text() == "3.5"
