from pages import SlowResourcesPage


def test_slow_resources_page_loads_after_delay(driver, base_url):
    """
    The /slow page includes a rogue GET request that takes ~30 seconds.
    Verify the page eventually loads fully and contains the expected content.
    """
    page = SlowResourcesPage(driver, base_url=base_url)

    elapsed = page.page_load_time(timeout=45)

    assert page.heading_text() == "Slow Resources"
    assert "30 seconds" in page.description_text()
    assert elapsed >= 5, f"Expected slow load, but page loaded in {elapsed:.1f}s"
