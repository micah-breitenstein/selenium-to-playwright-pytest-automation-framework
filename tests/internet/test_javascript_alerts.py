import pytest

from pages import JavaScriptAlertsPage


@pytest.mark.no_safari
def test_js_alert(driver, base_url):
    page = JavaScriptAlertsPage(driver, base_url).open()

    page.click_js_alert()
    page.accept_alert()

    assert page.result_text() == "You successfully clicked an alert"


@pytest.mark.no_safari
def test_js_confirm_ok(driver, base_url):
    page = JavaScriptAlertsPage(driver, base_url).open()

    page.click_js_confirm()
    page.accept_alert()

    assert page.result_text() == "You clicked: Ok"


@pytest.mark.no_safari
def test_js_confirm_cancel(driver, base_url):
    page = JavaScriptAlertsPage(driver, base_url).open()

    page.click_js_confirm()
    page.dismiss_alert()

    assert page.result_text() == "You clicked: Cancel"


@pytest.mark.no_safari
def test_js_prompt(driver, base_url):
    page = JavaScriptAlertsPage(driver, base_url).open()

    page.click_js_prompt()
    page.send_text_to_prompt("Micah")

    assert page.result_text() == "You entered: Micah"
