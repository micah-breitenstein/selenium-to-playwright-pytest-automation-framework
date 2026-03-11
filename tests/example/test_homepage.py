import time

from pages.example import HomePage


def test_homepage_heading_example(driver, base_url):
    """Test that example.com loads and displays the expected heading."""
    homepage = HomePage(driver, base_url=base_url)

    # example.com is external and can be unreliable under heavy parallel load
    for attempt in range(3):
        homepage.load()
        try:
            text = homepage.get_heading_text()
            if "can't be reached" not in text and "not available" not in text:
                break
        except Exception:
            pass
        if attempt < 2:
            time.sleep(2)

    assert homepage.get_heading_text() == "Example Domain"
