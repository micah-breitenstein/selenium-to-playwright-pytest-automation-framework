from pages import RedirectorPage


def test_redirector_navigates_to_status_codes(driver, base_url):
    page = RedirectorPage(driver, base_url=base_url).load()

    assert page.heading_text() == "Redirection"

    page.click_redirect()
    page.wait_for_url_contains("/status_codes")

    assert "/status_codes" in page.current_url()
