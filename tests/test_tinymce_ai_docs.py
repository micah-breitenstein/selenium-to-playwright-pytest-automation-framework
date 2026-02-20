import pytest

from pages import TinyMceAiDocsPage


def test_tinymce_ai_docs_demo_loads(driver):
    TinyMceAiDocsPage(driver).open().assert_phrase_in_editor("Try out AI Assistant!")


@pytest.mark.no_safari
def test_tinymce_docs_can_type_and_bold(driver):
    (
        TinyMceAiDocsPage(driver)
        .open()
        .format_bold("Hello TinyMCE")
        .assert_html_contains_any(["<strong>", "<b>"])
    )


@pytest.mark.no_safari
def test_tinymce_docs_can_type_and_italic(driver):
    (
        TinyMceAiDocsPage(driver)
        .open()
        .format_italic("Make me italic")
        .assert_html_contains_any(["<em>", "<i>"])
    )