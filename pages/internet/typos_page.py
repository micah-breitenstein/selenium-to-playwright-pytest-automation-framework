from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class TyposPage:
    URL_PATH = "/typos"
    HEADING = (By.CSS_SELECTOR, "h3")
    CONTENT = (By.CSS_SELECTOR, "#content")

    # The page randomly shows either the correct sentence or a typo'd version
    EXPECTED_SENTENCES = (
        "Sometimes you'll see a typo, other times you won't.",
        "Sometimes you'll see a typo, other times you won,t.",
    )

    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self) -> "TyposPage":
        self.driver.get(f"{self.base_url}{self.URL_PATH}")
        return self

    def heading_text(self) -> str:
        return self.driver.find_element(*self.HEADING).text.strip()

    def content_text(self) -> str:
        return self.driver.find_element(*self.CONTENT).text.strip()

    def has_expected_typos_sentence(self) -> bool:
        text = self.content_text()
        return any(sentence in text for sentence in self.EXPECTED_SENTENCES)
