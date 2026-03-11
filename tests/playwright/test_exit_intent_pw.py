from __future__ import annotations

import pytest

from pages.internet import PWExitIntentPage


@pytest.mark.playwright
def test_exit_intent_modal_appears_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWExitIntentPage).open()
    page.trigger_exit_intent()
    page.wait_for_modal(timeout_ms=5_000)
    assert "MODAL" in page.modal_title().upper()
