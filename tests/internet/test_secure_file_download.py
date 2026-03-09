import pytest

from pages import SecureFileDownloadPage


@pytest.mark.no_safari
def test_secure_file_download_with_valid_credentials(driver, base_url):
    page = SecureFileDownloadPage(driver, base_url)
    page.open_with_credentials("admin", "admin")

    assert page.heading_text() == "Secure File Downloader"


@pytest.mark.no_safari
def test_secure_file_download_lists_files(driver, base_url):
    page = SecureFileDownloadPage(driver, base_url)
    page.open_with_credentials("admin", "admin")

    files = page.file_names()
    assert len(files) >= 1, "Expected at least one file listed"


@pytest.mark.no_safari
def test_secure_file_download_file_accessible_with_auth(driver, base_url):
    page = SecureFileDownloadPage(driver, base_url)
    page.open_with_credentials("admin", "admin")

    hrefs = page.file_hrefs()
    assert hrefs, "Expected at least one download link"

    # Check first file is accessible with auth
    status = page.head_status_with_auth(hrefs[0], "admin", "admin")
    assert status == 200, f"Expected 200, got {status}"


@pytest.mark.no_safari
def test_secure_file_download_print_all_files(driver, base_url):
    page = SecureFileDownloadPage(driver, base_url)
    page.open_with_credentials("admin", "admin")

    files = page.file_names()
    print("\n--- Secure Download Files ---")
    for f in files:
        print(f"  {f}")
    print(f"--- Total: {len(files)} files ---")
