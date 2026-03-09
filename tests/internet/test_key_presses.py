import pytest
from selenium.webdriver.common.keys import Keys

from pages import KeyPressesPage


@pytest.mark.no_safari
@pytest.mark.parametrize(
    "key, expected",
    [
        (Keys.TAB, "TAB"),
        (Keys.ESCAPE, "ESCAPE"),
        (Keys.SPACE, "SPACE"),
        ("a", "A"),
        ("9", "9"),
    ],
)
def test_key_presses_result(driver, base_url, key, expected):
    page = KeyPressesPage(driver, base_url).open()
    result = page.press_and_wait_for(key, expected)
    assert result == f"You entered: {expected}"
