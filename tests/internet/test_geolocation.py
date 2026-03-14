import pytest

from pages.internet import GeolocationPage


@pytest.mark.no_safari
def test_geolocation_shows_mocked_coords(driver, base_url, mock_geolocation):
    latitude = 37.7749
    longitude = -122.4194

    mock_geolocation(latitude, longitude)
    page = GeolocationPage(driver, base_url=base_url).open().click_where_am_i()

    lat_text = page.lat_text()
    long_text = page.long_text()

    assert str(latitude) in lat_text
    assert str(longitude) in long_text
