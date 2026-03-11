from __future__ import annotations

import pytest

from pages.internet import PWGeolocationPage


@pytest.mark.playwright
def test_geolocation_shows_mocked_coords_playwright(pw_context, pw_page, base_url):
    latitude = 37.7749
    longitude = -122.4194

    pw_context.grant_permissions(["geolocation"], origin=base_url)
    pw_context.set_geolocation(
        {"latitude": latitude, "longitude": longitude, "accuracy": 10}
    )

    page = PWGeolocationPage(pw_page, base_url=base_url).open()
    page.click_where_am_i().wait_for_coordinates()

    assert str(latitude) in page.lat_text()
    assert str(longitude) in page.long_text()
