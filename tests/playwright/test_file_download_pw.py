from __future__ import annotations

import logging
import re

import pytest

from pages.internet import PWFileDownloadPage

log = logging.getLogger(__name__)

PATTERN = re.compile(r"^LAKETAHOECAVEROCK_[0-9a-fA-F]{8}\.JPG$")


@pytest.mark.playwright
def test_download_links_return_200_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWFileDownloadPage).open()

    file_names = page.file_names()
    hrefs = page.file_hrefs()

    assert hrefs, "No download links found on /download"

    log.info("Found %d download files:", len(file_names))
    for name in file_names:
        log.info(" - %s", name)

    to_check = hrefs[:5]

    failures = []
    for url in to_check:
        status = page.head_status(url)
        log.info("Checked %s -> status %s", url, status)
        if status != 200:
            failures.append((url, status))

    assert not failures, f"Some download links did not return 200: {failures}"


@pytest.mark.playwright
def test_target_file_presence_logs_only_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWFileDownloadPage).open()
    file_names = page.file_names()

    matches = [name for name in file_names if PATTERN.match(name)]

    if matches:
        log.info("Matching file(s) found:")
        for match in matches:
            log.info(" - %s", match)
    else:
        log.info("No matching files found.")

    assert True
