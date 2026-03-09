from pages import InputsPage


def test_inputs_accepts_typing(driver, base_url):
    page = InputsPage(driver, base_url).open()
    page.set_number(123)
    assert page.value() == "123"


def test_inputs_accepts_negative(driver, base_url):
    page = InputsPage(driver, base_url).open()
    page.set_number(-7)
    assert page.value() == "-7"


def test_inputs_increment_decrement(driver, base_url):
    page = InputsPage(driver, base_url).open()
    page.set_number(10)

    page.increment(3)
    assert page.value() == "13"

    page.decrement(5)
    assert page.value() == "8"
