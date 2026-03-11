from __future__ import annotations

import time

from pages.core.pw_base_page import PWBasePage


class PWSlowResourcesPage(PWBasePage):
    URL_PATH = "/slow"

    HEADING = "#content h3"
    DESCRIPTION = "#content .example p"

    _AJAX_DONE_JS = "(typeof jQuery !== 'undefined') && (jQuery.active === 0)"

    def _wait_for_ajax(self, timeout_ms: int = 45_000) -> None:
        self.page.wait_for_function(self._AJAX_DONE_JS, timeout=timeout_ms)

    def load(self, timeout_ms: int = 45_000) -> "PWSlowResourcesPage":
        self.go(self.URL_PATH)
        self._wait_for_ajax(timeout_ms=timeout_ms)
        return self

    def heading_text(self) -> str:
        return self.get_text(self.HEADING)

    def description_text(self) -> str:
        return self.get_text(self.DESCRIPTION)

    def page_load_time(self, timeout_ms: int = 45_000) -> float:
        start = time.time()
        self.go(self.URL_PATH)
        self._wait_for_ajax(timeout_ms=timeout_ms)
        return time.time() - start
