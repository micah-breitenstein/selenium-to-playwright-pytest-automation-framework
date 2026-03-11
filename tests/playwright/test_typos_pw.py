from __future__ import annotations

import pytest

from pages.internet import PWTyposPage


@pytest.mark.playwright
def test_typos_page_loads_and_shows_expected_sentence_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWTyposPage).open()

    assert page.heading_text() == "Typos"
    assert page.has_expected_typos_sentence()
