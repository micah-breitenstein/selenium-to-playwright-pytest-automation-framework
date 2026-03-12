from __future__ import annotations

import pytest

from pages.internet import PWInputsPage


@pytest.mark.playwright
def test_inputs_accepts_typing_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWInputsPage).open()
    page.set_number(123)
    assert page.value() == "123"


@pytest.mark.playwright
def test_inputs_accepts_negative_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWInputsPage).open()
    page.set_number(-7)
    assert page.value() == "-7"


@pytest.mark.playwright
def test_inputs_increment_decrement_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWInputsPage).open()
    page.set_number(10)

    page.increment(3)
    assert page.value() == "13"

    page.decrement(5)
    assert page.value() == "8"
