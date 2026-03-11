from __future__ import annotations

import pytest

from pages.internet import PWNestedFramesPage


@pytest.mark.playwright
def test_nested_frames_texts_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWNestedFramesPage).open()

    assert page.left_text() == "LEFT"
    assert page.middle_text() == "MIDDLE"
    assert page.right_text() == "RIGHT"
    assert page.bottom_text() == "BOTTOM"
