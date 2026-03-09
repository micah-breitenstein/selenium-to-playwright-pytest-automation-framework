from pages import ShiftingContentImagePage


def test_shifting_content_image_heading(driver, base_url):
    page = ShiftingContentImagePage(driver, base_url=base_url).load()

    assert page.heading_text() == "Shifting Content: Image"


def test_shifting_content_image_default(driver, base_url):
    page = ShiftingContentImagePage(driver, base_url=base_url).load()

    assert "/img/avatar.jpg" in page.image_src()
    assert page.current_url().endswith("/shifting_content/image")


def test_shifting_content_image_random_mode(driver, base_url):
    page = ShiftingContentImagePage(driver, base_url=base_url).load_random()

    assert "/img/avatar.jpg" in page.image_src()
    assert "mode=random" in page.current_url()


def test_shifting_content_image_pixel_shift_mode(driver, base_url):
    page = ShiftingContentImagePage(driver, base_url=base_url).load_with_pixel_shift(100)

    assert "/img/avatar.jpg" in page.image_src()
    assert "pixel_shift=100" in page.current_url()


def test_shifting_content_image_random_and_pixel_shift_mode(driver, base_url):
    page = ShiftingContentImagePage(driver, base_url=base_url).load_random_with_pixel_shift(100)

    assert "/img/avatar.jpg" in page.image_src()
    current = page.current_url()
    assert "mode=random" in current
    assert "pixel_shift=100" in current
