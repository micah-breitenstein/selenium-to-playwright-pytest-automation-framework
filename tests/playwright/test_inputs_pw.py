from __future__ import annotations

import pytest

from pages.internet import PWInputsPage


@pytest.mark.playwright
def test_inputs_accepts_typing_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWInputsPage).open()
    page.set_number(123)
    assert page.value() == "123"
