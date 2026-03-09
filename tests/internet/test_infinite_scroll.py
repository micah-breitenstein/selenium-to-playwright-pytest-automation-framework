from pages import InfiniteScrollPage


def test_infinite_scroll_loads_more_content(driver, base_url):
    page = InfiniteScrollPage(driver, base_url).open()

    page.load_blocks(target_blocks=15)

    assert page.block_count() >= 15