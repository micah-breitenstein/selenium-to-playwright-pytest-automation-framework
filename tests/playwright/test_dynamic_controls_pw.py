from __future__ import annotations

import pytest

from pages.internet import PWDynamicControlsPage


@pytest.mark.playwright
def test_dynamic_controls_checkbox_toggle_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDynamicControlsPage).open()

    assert page.is_checkbox_visible()

    page.toggle_checkbox()
    assert "gone" in page.message_text().lower()
    assert not page.is_checkbox_visible()

    page.toggle_checkbox()
    assert "back" in page.message_text().lower()
    assert page.is_checkbox_visible()


@pytest.mark.playwright
def test_dynamic_controls_enable_disable_input_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDynamicControlsPage).open()

    assert not page.is_input_enabled()

    page.enable_input()
    assert "enabled" in page.message_text().lower()
    assert page.is_input_enabled()

    page.disable_input()
    assert "disabled" in page.message_text().lower()
    assert not page.is_input_enabled()
