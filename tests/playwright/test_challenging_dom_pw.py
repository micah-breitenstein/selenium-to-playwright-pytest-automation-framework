from __future__ import annotations

import pytest

from pages.internet import PWChallengingDomPage


@pytest.mark.playwright
def test_challenging_dom_has_three_buttons_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWChallengingDomPage).open()
    texts = page.button_texts()
    assert set(texts.keys()) == {"blue", "red", "green"}
    assert all(texts[color] for color in texts), (
        f"Expected all button texts to be non-empty, got: {texts}"
    )
