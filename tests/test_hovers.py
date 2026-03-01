from pages import HoversPage


def test_hover_reveals_user1_name_and_link(driver, base_url):
    page = HoversPage(driver, base_url).open()

    page.hover_user(1)

    assert page.user_name_text(1) == "name: user1"
    assert page.user_profile_href(1).endswith("/users/1")


def test_click_view_profile_navigates(driver, base_url):
    page = HoversPage(driver, base_url).open()

    page.hover_user(2)
    page.click_view_profile(2)

    assert driver.current_url.endswith("/users/2")