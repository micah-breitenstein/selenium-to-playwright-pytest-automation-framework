from pages import ShiftingContentMenuPage


EXPECTED_MENU_ITEMS = ["Home", "About", "Contact Us", "Portfolio", "Gallery"]


def test_shifting_content_menu_heading(driver, base_url):
    page = ShiftingContentMenuPage(driver, base_url=base_url).load()

    assert page.heading_text() == "Shifting Content: Menu Element"


def test_shifting_content_menu_items_default(driver, base_url):
    page = ShiftingContentMenuPage(driver, base_url=base_url).load()

    assert page.menu_items() == EXPECTED_MENU_ITEMS
    assert page.current_url().endswith("/shifting_content/menu")


def test_shifting_content_menu_items_random_mode(driver, base_url):
    page = ShiftingContentMenuPage(driver, base_url=base_url).load_random()

    assert page.menu_items() == EXPECTED_MENU_ITEMS
    assert "mode=random" in page.current_url()


def test_shifting_content_menu_items_pixel_shift_mode(driver, base_url):
    page = ShiftingContentMenuPage(driver, base_url=base_url).load_with_pixel_shift(100)

    assert page.menu_items() == EXPECTED_MENU_ITEMS
    assert "pixel_shift=100" in page.current_url()


def test_shifting_content_menu_items_random_and_pixel_shift_mode(driver, base_url):
    page = ShiftingContentMenuPage(driver, base_url=base_url).load_random_with_pixel_shift(100)

    assert page.menu_items() == EXPECTED_MENU_ITEMS
    current = page.current_url()
    assert "mode=random" in current
    assert "pixel_shift=100" in current
