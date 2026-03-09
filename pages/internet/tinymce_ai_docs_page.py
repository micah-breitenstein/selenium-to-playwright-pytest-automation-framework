from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class TinyMceAiDocsPage:
    """
    Automates Tiny Cloud docs AI interactive example.

    This is a 3rd-party docs embed with nested iframes and occasional overlays.
    We:
      - anchor on #live-demo_ai
      - switch into its iframe
      - optionally click a start/run overlay
      - recurse frames to find editor content/phrases
      - interact with editor + toolbar and assert resulting HTML
    """

    URL = "https://www.tiny.cloud/docs/tinymce/6/ai/#interactive-example"

    LIVE_DEMO_CONTAINER = (By.CSS_SELECTOR, "#live-demo_ai > div.content")
    OUTER_IFRAME_IN_CONTAINER = (By.CSS_SELECTOR, "iframe")

    # TinyMCE UI / editor locators (inside the demo iframe)
    TOOLBAR_BOLD = (By.CSS_SELECTOR, "button[aria-label='Bold'], button[title='Bold']")
    TOOLBAR_ITALIC = (By.CSS_SELECTOR, "button[aria-label='Italic'], button[title='Italic']")
    EDIT_IFRAME = (By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")
    EDITOR_BODY = (By.CSS_SELECTOR, "body#tinymce")

    def __init__(self, driver):
        self.driver = driver

    # -------------------------
    # Navigation
    # -------------------------
    def open(self, timeout: int = 60) -> "TinyMceAiDocsPage":
        self.driver.get(self.URL)
        wait = WebDriverWait(self.driver, timeout)

        container = wait.until(lambda d: d.find_element(*self.LIVE_DEMO_CONTAINER))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", container)

        outer = wait.until(lambda d: container.find_element(*self.OUTER_IFRAME_IN_CONTAINER))
        self.driver.switch_to.frame(outer)

        # best-effort; harmless if not present
        self._maybe_click_start_overlay()

        return self

    # -------------------------
    # Assertions
    # -------------------------
    def assert_phrase_in_editor(self, phrase: str, timeout: int = 20) -> "TinyMceAiDocsPage":
        found = self._find_frame_containing_phrase(phrase, timeout=timeout)
        assert found, f"Could not find phrase in demo iframe or its child frames: {phrase!r}"
        return self

    def assert_html_contains_any(self, needles: list[str], timeout: int = 20) -> "TinyMceAiDocsPage":
        html = self.editor_html(timeout=timeout)
        assert any(n in html for n in needles), f"None of {needles!r} found in editor HTML."
        return self

    # -------------------------
    # Editor interactions
    # -------------------------
    def set_plain_text(self, text: str, timeout: int = 20) -> "TinyMceAiDocsPage":
        self._switch_to_demo_iframe_root()
        body = self._switch_to_editor_body(timeout=timeout)

        body.click()
        body.send_keys(Keys.COMMAND, "a")
        body.send_keys(text)
        return self

    def select_all_in_editor(self, timeout: int = 20) -> "TinyMceAiDocsPage":
        self._switch_to_demo_iframe_root()
        body = self._switch_to_editor_body(timeout=timeout)

        body.click()
        body.send_keys(Keys.COMMAND, "a")
        return self

    def click_bold(self, timeout: int = 20) -> "TinyMceAiDocsPage":
        self._switch_to_demo_iframe_root()
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: d.find_element(*self.TOOLBAR_BOLD)).click()
        return self

    def click_italic(self, timeout: int = 20) -> "TinyMceAiDocsPage":
        self._switch_to_demo_iframe_root()
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: d.find_element(*self.TOOLBAR_ITALIC)).click()
        return self

    def editor_html(self, timeout: int = 20) -> str:
        self._switch_to_demo_iframe_root()
        body = self._switch_to_editor_body(timeout=timeout)
        return self.driver.execute_script("return arguments[0].innerHTML;", body)

    # -------------------------
    # Fluent helpers
    # -------------------------
    def format_bold(self, text: str, timeout: int = 20) -> "TinyMceAiDocsPage":
        return (
            self.set_plain_text(text, timeout=timeout)
                .select_all_in_editor(timeout=timeout)
                .click_bold(timeout=timeout)
        )

    def format_italic(self, text: str, timeout: int = 20) -> "TinyMceAiDocsPage":
        return (
            self.set_plain_text(text, timeout=timeout)
                .select_all_in_editor(timeout=timeout)
                .click_italic(timeout=timeout)
        )

    # -------------------------
    # Internal helpers
    # -------------------------
    def _maybe_click_start_overlay(self) -> bool:
        candidates = [
            (By.XPATH, "//button[contains(., 'Run')]"),
            (By.XPATH, "//button[contains(., 'Start')]"),
            (By.XPATH, "//button[contains(., 'Load')]"),
            (By.XPATH, "//button[contains(., 'Play')]"),
            (By.CSS_SELECTOR, "button[aria-label*='Run']"),
        ]
        for by, sel in candidates:
            try:
                el = self.driver.find_element(by, sel)
                if el.is_displayed() and el.is_enabled():
                    el.click()
                    return True
            except Exception:
                pass
        return False

    def _switch_to_demo_iframe_root(self) -> None:
        """
        Ensures we're in the outer demo iframe (toolbar lives here).
        If we're inside the inner edit iframe, one parent_frame() gets us back.
        """
        try:
            self.driver.switch_to.parent_frame()
        except Exception:
            pass

    def _switch_to_editor_body(self, timeout: int = 20):
        """
        From the demo iframe root -> inner edit iframe -> body#tinymce.
        Leaves driver inside the inner iframe.
        """
        wait = WebDriverWait(self.driver, timeout)
        edit_iframe = wait.until(lambda d: d.find_element(*self.EDIT_IFRAME))
        self.driver.switch_to.frame(edit_iframe)
        return wait.until(lambda d: d.find_element(*self.EDITOR_BODY))

    def _find_frame_containing_phrase(self, phrase: str, timeout: int = 20) -> bool:
        """
        Starting from current frame context, search this frame and its child iframes
        for either:
          - body#tinymce containing phrase
          - any body containing phrase
        If found, leaves driver inside the matching frame.
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: d.find_elements(By.TAG_NAME, "body"))

        # direct in this frame
        try:
            if self.driver.find_elements(*self.EDITOR_BODY):
                body = self.driver.find_element(*self.EDITOR_BODY)
                if phrase in (body.text or ""):
                    return True
        except Exception:
            pass

        try:
            body = self.driver.find_element(By.TAG_NAME, "body")
            if phrase in (body.text or ""):
                return True
        except Exception:
            pass

        # recurse
        frames = self.driver.find_elements(By.CSS_SELECTOR, "iframe")
        for fr in frames:
            try:
                self.driver.switch_to.frame(fr)
                if self._find_frame_containing_phrase(phrase, timeout=timeout):
                    return True
            except Exception:
                pass
            finally:
                self.driver.switch_to.parent_frame()

        return False