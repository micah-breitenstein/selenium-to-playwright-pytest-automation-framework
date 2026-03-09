# tests/test_jqueryui_menu.py
import pytest

from pages import JQueryUIMenuPage


@pytest.mark.no_safari
def test_pdf_download_href(driver, base_url):
    page = JQueryUIMenuPage(driver, base_url).open()
    href = page.pdf_href()
    assert href.endswith("menu.pdf"), f"Unexpected href: {href}"


@pytest.mark.no_safari
def test_csv_download_href(driver, base_url):
    page = JQueryUIMenuPage(driver, base_url).open()
    href = page.csv_href()
    assert href.endswith("menu.csv"), f"Unexpected href: {href}"


@pytest.mark.no_safari
def test_excel_download_href(driver, base_url):
    page = JQueryUIMenuPage(driver, base_url).open()
    href = page.excel_href()
    assert href.endswith("menu.xls"), f"Unexpected href: {href}"


@pytest.mark.no_safari
def test_back_to_jquery_href(driver, base_url):
    page = JQueryUIMenuPage(driver, base_url).open()
    href = page.back_to_jquery_href()

    assert href == f"{base_url.rstrip('/')}/jqueryui", f"Unexpected href: {href}"
