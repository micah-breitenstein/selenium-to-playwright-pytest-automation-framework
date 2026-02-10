from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.core.base_page import BasePage


class JavaScriptErrorPage(BasePage):
    URL_PATH = "/javascript_error"

    BODY = (By.TAG_NAME, "body")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_logs: list[dict] | None = None

    def load(self) -> "JavaScriptErrorPage":
        self._cached_logs = None  # Reset cache on load
        self.go(self.URL_PATH)
        self.wait_visible(self.BODY)
        return self

    def body_text(self) -> str:
        return self.get_text(self.BODY).strip()

    def get_browser_logs(self) -> list[dict]:
        """
        Returns browser console logs. Only works on Chrome/Chromium.
        Safari and Firefox do not support this via WebDriver.
        Note: Browser logs are consumed on read, so we cache them.
        """
        if self._cached_logs is not None:
            return self._cached_logs
        try:
            self._cached_logs = self.driver.get_log("browser")
        except Exception:
            self._cached_logs = []
        return self._cached_logs

    def has_javascript_error(self) -> bool:
        """Check if any SEVERE level JS errors exist in browser logs."""
        logs = self.get_browser_logs()
        return any(log.get("level") == "SEVERE" for log in logs)

    def javascript_error_messages(self) -> list[str]:
        """Return all SEVERE level error messages from browser logs."""
        logs = self.get_browser_logs()
        return [log.get("message", "") for log in logs if log.get("level") == "SEVERE"]
