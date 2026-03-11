from __future__ import annotations

import pytest

from pages.internet import PWJQueryUIMenuPage


@pytest.mark.playwright
def test_pdf_download_href_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJQueryUIMenuPage).open()
    href = page.pdf_href()
    assert href.endswith("menu.pdf"), f"Unexpected href: {href}"


@pytest.mark.playwright
def test_csv_download_href_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJQueryUIMenuPage).open()
    href = page.csv_href()
    assert href.endswith("menu.csv"), f"Unexpected href: {href}"


@pytest.mark.playwright
def test_excel_download_href_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWJQueryUIMenuPage).open()
    href = page.excel_href()
    assert href.endswith("menu.xls"), f"Unexpected href: {href}"


@pytest.mark.playwright
def test_back_to_jquery_href_playwright(pw_page_object_factory, base_url: str):
    page = pw_page_object_factory(PWJQueryUIMenuPage).open()
    href = page.back_to_jquery_href()
    assert href == f"{base_url.rstrip('/')}/jqueryui", f"Unexpected href: {href}"
