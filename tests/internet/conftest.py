# tests/internet/conftest.py
"""
Fixtures specific to the-internet.herokuapp.com test suite.
"""
from __future__ import annotations

import pytest


@pytest.fixture
def internet_page(page):
    """
    Convenience wrapper around the generic ``page`` factory.

    Usage::

        def test_example(internet_page):
            login = internet_page(LoginPage)
            login.go("/login")
    """
    return page


@pytest.fixture
def navigate(landing):
    """
    Return the landing page already loaded and ready for navigation.

    Usage::

        def test_checkboxes(navigate):
            cb = navigate.go_to_checkboxes()
    """
    return landing.load()
