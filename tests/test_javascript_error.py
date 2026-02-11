import pytest

from pages import JavaScriptErrorPage


@pytest.mark.no_safari
def test_javascript_error_page_has_js_error(driver, base_url):
    """
    The /javascript_error page intentionally throws a JS error on load.
    This test verifies we can detect it via browser logs (Chrome only).
    """
    page = JavaScriptErrorPage(driver, base_url=base_url).load()

    assert page.has_javascript_error(), "Expected a JavaScript error in browser logs"

    errors = page.javascript_error_messages()
    assert len(errors) >= 1, "Expected at least one JS error message"
    # The page throws "Cannot read properties of undefined (reading 'xyz')" or similar
    assert any("undefined" in msg.lower() or "error" in msg.lower() for msg in errors), \
        f"Expected JS error about undefined, got: {errors}"


@pytest.mark.no_safari
def test_javascript_error_page_loads(driver, base_url):
    """Page should still load despite the JS error."""
    page = JavaScriptErrorPage(driver, base_url=base_url).load()

    # The page has minimal content but should have a body
    assert page.body_text() is not None
