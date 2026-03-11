from __future__ import annotations

import pytest
import requests
from requests.auth import HTTPBasicAuth

from pages.internet import PWBasicAuthPage


@pytest.mark.playwright
def test_basic_auth_success_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWBasicAuthPage).open_with_credentials(
        "admin", "admin"
    )
    assert "Congratulations" in page.get_message()


@pytest.mark.playwright
def test_basic_auth_failure_returns_401_playwright(base_url: str):
    url = f"{base_url.rstrip('/')}/basic_auth"
    response = requests.get(url, auth=HTTPBasicAuth("wrong", "wrong"), timeout=20)
    assert response.status_code == 401
