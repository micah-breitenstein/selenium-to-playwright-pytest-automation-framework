from pages import ShadowDomPage


def test_shadow_dom_page_loads(driver, base_url):
    page = ShadowDomPage(driver, base_url=base_url).load()

    assert "Simple template" in page.heading_text()


def test_shadow_dom_has_shadow_hosts(driver, base_url):
    page = ShadowDomPage(driver, base_url=base_url).load()

    count = page.shadow_host_count()
    assert count >= 1, f"Expected at least 1 shadow host, got {count}"


def test_shadow_dom_can_access_shadow_root(driver, base_url):
    page = ShadowDomPage(driver, base_url=base_url).load()

    shadow_root = page.get_shadow_root(0)
    assert shadow_root is not None, "Expected to access shadow root"


def test_shadow_dom_slot_content(driver, base_url):
    page = ShadowDomPage(driver, base_url=base_url).load()

    # Get the slotted content from light DOM
    content = page.get_shadow_slot_content(0)
    assert content, "Expected slotted content in shadow host"
