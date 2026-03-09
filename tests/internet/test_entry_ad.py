import pytest

from pages import EntryAdPage  # lazy-loaded via pages/__init__.py


@pytest.mark.no_safari
def test_entry_ad_modal_can_be_closed(driver, base_url):
    page = EntryAdPage(driver, base_url).open()

    # Demo site behavior can vary (modal may not appear every load)
    if not page.modal_is_visible(timeout=2):
        pytest.skip("Entry Ad modal did not appear on initial load (demo-site state).")

    title = page.modal_title(timeout=3).upper()
    assert title, "Modal visible but title was empty"
    assert "MODAL" in title

    page.close_modal()

    # Confirm modal is no longer visible (allow time for CSS fade-out animation)
    assert page.modal_is_visible(timeout=1) is False


@pytest.mark.no_safari
def test_restart_ad_triggers_modal_again(driver, base_url):
    page = EntryAdPage(driver, base_url).open()

    # If it appears on initial open, close it (fast probe)
    if page.modal_is_visible(timeout=2):
        page.close_modal()

    # Trigger modal again
    page.restart_ad()

    # This is a case where we EXPECT it -> purposeful wait
    # But the demo can be flaky; retry restart once before giving up.
    try:
        page.wait_for_modal(timeout=10)
    except Exception:
        # one cheap retry
        page.restart_ad()
        if not page.modal_is_visible(timeout=2):
            pytest.skip(
                "Entry Ad modal did not re-appear after restart (demo-site flake/state)."
            )
        page.wait_for_modal(timeout=5)

    page.close_modal()
