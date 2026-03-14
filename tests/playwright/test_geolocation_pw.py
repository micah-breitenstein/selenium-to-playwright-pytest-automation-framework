from __future__ import annotations

import pytest

from pages.internet import PWGeolocationPage
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


@pytest.mark.playwright
@pytest.mark.parametrize(("latitude", "longitude"), CITIES)
def test_geolocation_shows_mocked_coords_for_city_playwright(
    pw_mock_geolocation, pw_page, base_url, latitude, longitude
):
    pw_mock_geolocation(latitude, longitude)

    page = PWGeolocationPage(pw_page, base_url=base_url).open()
    page.click_where_am_i().wait_for_coordinates()

    assert str(latitude) in page.lat_text()
    assert str(longitude) in page.long_text()


@pytest.mark.playwright
def test_geolocation_is_within_2km_of_mocked_point_playwright(
    pw_mock_geolocation, pw_page, base_url
):
    latitude = 37.7749
    longitude = -122.4194

    pw_mock_geolocation(latitude, longitude)

    page = PWGeolocationPage(pw_page, base_url=base_url).open()
    page.click_where_am_i().wait_for_coordinates()

    actual_lat = parse_coordinate(page.lat_text())
    actual_long = parse_coordinate(page.long_text())

    distance_km = haversine_km(latitude, longitude, actual_lat, actual_long)
    assert distance_km <= 2.0


@pytest.mark.playwright
def test_geolocation_coordinates_are_in_valid_numeric_ranges_playwright(
    pw_mock_geolocation, pw_page, base_url
):
    latitude = 47.6062
    longitude = -122.3321

    pw_mock_geolocation(latitude, longitude)

    page = PWGeolocationPage(pw_page, base_url=base_url).open()
    page.click_where_am_i().wait_for_coordinates()

    actual_lat = parse_coordinate(page.lat_text())
    actual_long = parse_coordinate(page.long_text())

    assert coordinates_in_valid_range(actual_lat, actual_long)
