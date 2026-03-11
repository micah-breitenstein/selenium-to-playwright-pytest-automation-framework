from __future__ import annotations

import pytest

from pages.internet import PWSecureFileDownloadPage


@pytest.mark.playwright
def test_secure_file_download_with_valid_credentials_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWSecureFileDownloadPage).open_with_credentials(
        "admin", "admin"
    )
    assert page.heading_text() == "Secure File Downloader"


@pytest.mark.playwright
def test_secure_file_download_lists_files_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWSecureFileDownloadPage).open_with_credentials(
        "admin", "admin"
    )
    files = page.file_names()
    assert len(files) >= 1, "Expected at least one file listed"


@pytest.mark.playwright
def test_secure_file_download_file_accessible_with_auth_playwright(
    pw_page_object_factory,
):
    page = pw_page_object_factory(PWSecureFileDownloadPage).open_with_credentials(
        "admin", "admin"
    )
    hrefs = page.file_hrefs()
    assert hrefs, "Expected at least one download link"

    status = page.head_status_with_auth(hrefs[0], "admin", "admin")
    assert status == 200, f"Expected 200, got {status}"


@pytest.mark.playwright
def test_secure_file_download_print_all_files_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWSecureFileDownloadPage).open_with_credentials(
        "admin", "admin"
    )
    files = page.file_names()

    print("\n--- Secure Download Files ---")
    for filename in files:
        print(f"  {filename}")
    print(f"--- Total: {len(files)} files ---")
