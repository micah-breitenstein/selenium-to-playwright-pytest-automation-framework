from pages import NotificationMessagePage


def test_notification_message_appears(driver, base_url):
    page = NotificationMessagePage(driver, base_url=base_url).load()

    assert page.heading_text() == "Notification Message"

    page.click_to_load_message()
    text = page.notification_text()

    # The demo site randomly shows one of these messages
    valid_messages = ["Action successful", "Action unsuccesful, please try again"]
    assert any(msg in text for msg in valid_messages), f"Unexpected notification: {text!r}"


def test_notification_message_changes_on_click(driver, base_url):
    page = NotificationMessagePage(driver, base_url=base_url).load()

    messages = set()
    for _ in range(10):
        page.click_to_load_message()
        messages.add(page.notification_text())

    # Should see at least one message after multiple clicks
    assert len(messages) >= 1
