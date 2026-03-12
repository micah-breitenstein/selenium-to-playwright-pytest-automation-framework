from __future__ import annotations

import pytest

from pages.internet import PWEntryAdPage


@pytest.mark.playwright
def test_entry_ad_modal_can_be_closed_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWEntryAdPage).open()

    if not page.modal_is_visible(timeout_ms=2000):
        pytest.skip("Entry Ad modal did not appear on initial load (demo-site state).")

    title = page.modal_title(timeout_ms=3000).upper()
    assert title, "Modal visible but title was empty"
    assert "MODAL" in title

    page.close_modal()
    assert page.modal_is_visible(timeout_ms=1000) is False


@pytest.mark.playwright
def test_restart_ad_triggers_modal_again_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWEntryAdPage).open()

    if page.modal_is_visible(timeout_ms=2000):
        page.close_modal()

    page.restart_ad()

    try:
        page.wait_for_modal(timeout_ms=10000)
    except Exception:
        page.restart_ad()
        if not page.modal_is_visible(timeout_ms=2000):
            pytest.skip(
                "Entry Ad modal did not re-appear after restart (demo-site flake/state)."
            )
        page.wait_for_modal(timeout_ms=5000)

    page.close_modal()
