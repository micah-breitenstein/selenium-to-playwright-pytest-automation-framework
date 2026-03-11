import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages import TyposPage


@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,800")
    d = webdriver.Chrome(options=opts)
    d.implicitly_wait(2)
    yield d
    d.quit()


def test_typos_page_heading(driver, base_url):
    page = TyposPage(driver, base_url).open()
    assert page.heading_text() == "Typos"


def test_typos_page_shows_expected_sentence(driver, base_url):
    page = TyposPage(driver, base_url).open()
    assert page.has_expected_typos_sentence()
