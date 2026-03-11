from __future__ import annotations

from pathlib import Path

import pytest

from pages.internet import PWFileUploadPage

ORIGINAL_FILE = Path("test_file/LAKETAHOECAVEROCK.JPG")


@pytest.mark.playwright
def test_file_upload_unique_name_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWFileUploadPage).open()

    unique_name = page.upload_file_with_unique_name(ORIGINAL_FILE)

    assert page.upload_success_message() == "File Uploaded!"
    assert page.uploaded_filename() == unique_name
