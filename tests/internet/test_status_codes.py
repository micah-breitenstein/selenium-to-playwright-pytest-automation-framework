import pytest

from pages import StatusCodesPage


@pytest.mark.parametrize("code", [200, 301, 404, 500])
def test_status_code_page_displays_message(driver, base_url, code):
    page = StatusCodesPage(driver, base_url=base_url).load()
    page.click_code(code)

    assert f"/status_codes/{code}" in page.current_url()
    assert str(code) in page.result_text()


def test_status_codes_landing_heading(driver, base_url):
    page = StatusCodesPage(driver, base_url=base_url).load()

    assert page.heading_text() == "Status Codes"


def test_status_codes_return_link(driver, base_url):
    page = StatusCodesPage(driver, base_url=base_url).load()
    page.click_code(200)
    page.click_here_to_return()

    assert page.heading_text() == "Status Codes"
    assert page.current_url().endswith("/status_codes")
