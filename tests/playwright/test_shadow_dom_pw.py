from __future__ import annotations

import pytest

from pages.internet import PWShadowDomPage


@pytest.mark.playwright
def test_shadow_dom_has_shadow_hosts_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShadowDomPage).load()
    count = page.shadow_host_count()
    assert count >= 1, f"Expected at least 1 shadow host, got {count}"


@pytest.mark.playwright
def test_shadow_dom_page_loads_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShadowDomPage).load()
    assert "Simple template" in page.heading_text()


@pytest.mark.playwright
def test_shadow_dom_can_access_shadow_root_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShadowDomPage).load()
    has_root = page.page.locator("my-paragraph").first.evaluate("el => !!el.shadowRoot")
    assert has_root is True, "Expected to access shadow root"


@pytest.mark.playwright
def test_shadow_dom_slot_content_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWShadowDomPage).load()
    content = page.page.locator("my-paragraph").first.evaluate(
        """
        el => {
            if (!el.shadowRoot) return '';
            const slot = el.shadowRoot.querySelector('slot');
            if (!slot) return '';
            const nodes = slot.assignedNodes({ flatten: true });
            return nodes.map(n => n.textContent || '').join(' ').trim();
        }
        """
    )
    assert content, "Expected slotted content in shadow host"
