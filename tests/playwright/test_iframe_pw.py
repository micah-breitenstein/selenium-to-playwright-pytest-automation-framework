from __future__ import annotations

import logging

import pytest

from pages.internet import PWIFramePage

log = logging.getLogger(__name__)


@pytest.mark.playwright
def test_iframe_initial_text_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWIFramePage).open()

    if page.is_read_only():
        pytest.skip("TinyMCE editor is read-only (public demo state).")

    text = page.get_editor_text(wait_for_content=True)

    if not text.strip():
        pytest.skip("TinyMCE editor text was empty (public demo flake).")

    assert "Your content goes here." in text


@pytest.mark.playwright
def test_iframe_text_can_be_updated_or_is_read_only_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWIFramePage).open()

    if page.is_read_only():
        log.warning(
            "TinyMCE editor is in read-only mode (quota or disabled state). "
            "Skipping edit assertion."
        )
        pytest.skip("TinyMCE editor is read-only (quota or disabled state).")

    new_text = "Micah was here."
    page.set_editor_text(new_text)

    updated = page.get_editor_text(wait_for_content=True)
    assert updated == new_text
