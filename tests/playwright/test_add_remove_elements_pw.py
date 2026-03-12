from __future__ import annotations

import pytest

from pages.internet import PWAddRemoveElementsPage


@pytest.mark.playwright
def test_add_one_delete_button_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWAddRemoveElementsPage)
    page.open()

    page.add_element()
    page.wait_for_delete_count(1)
    assert page.delete_count() == 1


@pytest.mark.playwright
def test_add_thirty_then_delete_one_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWAddRemoveElementsPage)
    page.open()

    page.add_element(times=30)
    page.wait_for_delete_count(30)
    assert page.delete_count() == 30

    page.click_delete_at_index(0)
    page.wait_for_delete_count(29)
    assert page.delete_count() == 29


@pytest.mark.playwright
def test_add_two_then_delete_all_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWAddRemoveElementsPage)
    page.open()

    page.add_element(times=2)
    page.wait_for_delete_count(2)

    while page.delete_count() > 0:
        page.click_delete_at_index(0)

    page.wait_for_delete_count(0)
    assert page.delete_count() == 0
