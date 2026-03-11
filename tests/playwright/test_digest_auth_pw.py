from __future__ import annotations

import pytest

from pages.internet import PWDigestAuthPage


@pytest.mark.playwright
def test_digest_auth_succeeds_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWDigestAuthPage).open_with_credentials()
    assert "digest_auth" in page.current_url
