from __future__ import annotations

import pytest

from pages.internet import PWNotificationMessagePage


@pytest.mark.playwright
def test_notification_message_appears_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWNotificationMessagePage).load()

    assert page.heading_text() == "Notification Message"

    page.click_to_load_message()
    text = page.notification_text()
    valid_messages = ["Action successful", "Action unsuccesful, please try again"]
    assert any(msg in text for msg in valid_messages), f"Unexpected notification: {text!r}"
