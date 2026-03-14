import pytest

from pages.internet import GeolocationPage
from tests.internet.geospatial import (
    coordinates_in_valid_range,
    haversine_km,
    parse_coordinate,
)


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


@pytest.mark.no_safari
def test_geolocation_is_within_2km_of_mocked_point(driver, base_url, mock_geolocation):
    latitude = 37.7749
    longitude = -122.4194

    mock_geolocation(latitude, longitude)
    page = (
        GeolocationPage(driver, base_url=base_url)
        .open()
        .click_where_am_i()
        .wait_for_coordinates()
    )

    actual_lat = parse_coordinate(page.lat_text())
    actual_long = parse_coordinate(page.long_text())

    distance_km = haversine_km(latitude, longitude, actual_lat, actual_long)
    assert distance_km <= 2.0


@pytest.mark.no_safari
def test_geolocation_coordinates_are_in_valid_numeric_ranges(
    driver, base_url, mock_geolocation
):
    latitude = 47.6062
    longitude = -122.3321

    mock_geolocation(latitude, longitude)
    page = (
        GeolocationPage(driver, base_url=base_url)
        .open()
        .click_where_am_i()
        .wait_for_coordinates()
    )

    actual_lat = parse_coordinate(page.lat_text())
    actual_long = parse_coordinate(page.long_text())

    assert coordinates_in_valid_range(actual_lat, actual_long)


