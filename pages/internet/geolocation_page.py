# pages/geolocation_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class GeolocationPage:
    URL_PATH = "/geolocation"
    BTN = (By.CSS_SELECTOR, "#content button")
    LAT = (By.ID, "lat-value")
    LONG = (By.ID, "long-value")

    def __init__(self, driver, base_url="https://the-internet.herokuapp.com"):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self):
        self.driver.get(self.base_url + self.URL_PATH)
        return self

    def click_where_am_i(self):
        self.driver.find_element(*self.BTN).click()
        return self

    def wait_for_coordinates(self, timeout: int = 10):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: d.find_element(*self.LAT).text.strip() != "")
        wait.until(lambda d: d.find_element(*self.LONG).text.strip() != "")
        return self

    def lat_text(self):
        return self.driver.find_element(*self.LAT).text.strip()

    def long_text(self):
        return self.driver.find_element(*self.LONG).text.strip()
