from pages import WindowsPage


def test_windows_opens_new_window(driver, base_url):
    page = WindowsPage(driver, base_url=base_url).load()

    original = page.current_handle()
    _new_handle = page.open_new_window()  # noqa: F841

    assert page.heading_text() == "New Window"

    page.close_current_window()
    page.switch_to_window(original)

    assert page.heading_text() == "Opening a new window"
