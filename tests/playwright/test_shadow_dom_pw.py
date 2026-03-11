from __future__ import annotations

import pytest

from pages.internet import PWShadowDomPage


@pytest.mark.playwright
def test_shadow_dom_has_shadow_hosts_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShadowDomPage).load()
    count = page.shadow_host_count()
    assert count >= 1, f"Expected at least 1 shadow host, got {count}"
