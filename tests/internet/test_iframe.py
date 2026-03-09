import logging

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages import IFramePage

log = logging.getLogger(__name__)


def test_iframe_initial_text(driver: WebDriver, base_url: str) -> None:
    """
    Verifies TinyMCE editor loads and (when demo is in a testable state) contains default text.
    Public demo may be read-only or empty; skip those states.
    """
    page = IFramePage(driver, base_url=base_url).open()

    if page.is_read_only():
        pytest.skip("TinyMCE editor is read-only (public demo state).")

    text = page.get_editor_text(wait_for_content=True)

    if not text.strip():
        pytest.skip("TinyMCE editor text was empty (public demo flake).")

    assert "Your content goes here." in text


def test_iframe_text_can_be_updated_or_is_read_only(
    driver: WebDriver, base_url: str
) -> None:
    """
    Attempts to update the TinyMCE editor text.
    On the public demo site, TinyMCE may be read-only due to quota/disabled state.
    """
    page = IFramePage(driver, base_url=base_url).open()

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
