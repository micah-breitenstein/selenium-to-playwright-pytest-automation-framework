from __future__ import annotations

import pytest

from pages.internet import PWTinyMceAiDocsPage


@pytest.mark.playwright
def test_tinymce_ai_docs_demo_loads_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWTinyMceAiDocsPage)
    page.open().assert_phrase_in_editor("Try out AI Assistant!")


@pytest.mark.playwright
def test_tinymce_docs_can_type_and_bold_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWTinyMceAiDocsPage)
    page.open()
    if not page.is_editor_interactive():
        pytest.skip("TinyMCE demo editor is unavailable or non-interactive.")
    page.format_bold("Hello TinyMCE").assert_html_contains_any(["<strong>", "<b>"])


@pytest.mark.playwright
def test_tinymce_docs_can_type_and_italic_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWTinyMceAiDocsPage)
    page.open()
    if not page.is_editor_interactive():
        pytest.skip("TinyMCE demo editor is unavailable or non-interactive.")
    page.format_italic("Make me italic").assert_html_contains_any(["<em>", "<i>"])
