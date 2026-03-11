from __future__ import annotations

import pytest

from pages.internet import PWSlowResourcesPage


@pytest.mark.playwright
def test_slow_resources_page_loads_after_delay_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWSlowResourcesPage)

    elapsed = page.page_load_time(timeout_ms=45_000)

    assert page.heading_text() == "Slow Resources"
    assert "30 seconds" in page.description_text()
    assert elapsed >= 5, f"Expected slow load, but page loaded in {elapsed:.1f}s"
