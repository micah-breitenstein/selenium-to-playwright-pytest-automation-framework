import pytest

from pages.internet import GeolocationPage


CITIES = [
    pytest.param(37.7749, -122.4194, id="san_francisco"),
    pytest.param(40.7128, -74.0060, id="new_york_city"),
    pytest.param(51.5074, -0.1278, id="london"),
]


@pytest.mark.no_safari
@pytest.mark.parametrize(("latitude", "longitude"), CITIES)
def test_geolocation_shows_mocked_coords_for_city(
    driver, base_url, mock_geolocation, latitude, longitude
):
    mock_geolocation(latitude, longitude)
    page = (
        GeolocationPage(driver, base_url=base_url)
        .open()
        .click_where_am_i()
        .wait_for_coordinates()
    )

    lat_text = page.lat_text()
    long_text = page.long_text()

    assert str(latitude) in lat_text
    assert str(longitude) in long_text
