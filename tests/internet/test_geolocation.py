import pytest
import json
import time
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

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

USER_LATITUDE = 37.77856749431774
USER_LONGITUDE = -121.94199279668368


def _google_maps_directions_url(
    origin_latitude: float,
    origin_longitude: float,
    destination_latitude: float,
    destination_longitude: float,
) -> str:
    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={origin_latitude},{origin_longitude}"
        f"&destination={destination_latitude},{destination_longitude}"
        "&travelmode=driving"
    )


def _parks_nearby(lat: float, lon: float, radius_m: int = 3000) -> list[dict]:
    query = f"""
    [out:json][timeout:25];
    (
      node[\"leisure\"=\"park\"](around:{radius_m},{lat},{lon});
      way[\"leisure\"=\"park\"](around:{radius_m},{lat},{lon});
      relation[\"leisure\"=\"park\"](around:{radius_m},{lat},{lon});
    );
    out center tags;
    """

    payload = urlencode({"data": query}).encode("utf-8")
    request = Request(
        "https://overpass-api.de/api/interpreter",
        data=payload,
        method="POST",
        headers={"User-Agent": "selenium-python-basics-geolocation-tests"},
    )

    try:
        with urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        pytest.skip(f"Overpass API unavailable for nearby-park lookup: {exc}")

    parks: list[dict] = []
    seen = set()
    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name", "Unnamed park")
        if not name or name == "Unnamed park":
            continue

        park_lat = element.get("lat")
        park_lon = element.get("lon")
        center = element.get("center", {})
        if park_lat is None:
            park_lat = center.get("lat")
        if park_lon is None:
            park_lon = center.get("lon")
        if park_lat is None or park_lon is None:
            continue

        key = (name, park_lat, park_lon)
        if key in seen:
            continue
        seen.add(key)

        distance_km = haversine_km(lat, lon, float(park_lat), float(park_lon))
        parks.append(
            {
                "name": name,
                "latitude": float(park_lat),
                "longitude": float(park_lon),
                "distance_km": distance_km,
            }
        )

    parks.sort(key=lambda park: park["distance_km"])
    return parks


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


@pytest.mark.no_safari
def test_geolocation_navigates_google_maps_top_10_named_parks(
    driver, base_url, mock_geolocation
):
    mock_geolocation(USER_LATITUDE, USER_LONGITUDE)
    page = (
        GeolocationPage(driver, base_url=base_url)
        .open()
        .click_where_am_i()
        .wait_for_coordinates()
    )

    actual_lat = parse_coordinate(page.lat_text())
    actual_long = parse_coordinate(page.long_text())
    parks = _parks_nearby(actual_lat, actual_long, radius_m=3000)

    if not parks:
        pytest.skip(f"No named parks found near ({actual_lat}, {actual_long})")

    parks_to_visit = parks[:10]
    print(
        f"Navigating top {len(parks_to_visit)} named parks for "
        f"({actual_lat}, {actual_long})"
    )
    for index, park in enumerate(parks_to_visit, start=1):
        maps_url = _google_maps_directions_url(
            actual_lat,
            actual_long,
            park["latitude"],
            park["longitude"],
        )
        print(
            f"[{index}] {park['name']} ({park['distance_km']:.2f} km) -> {maps_url}"
        )
        driver.get(maps_url)
        time.sleep(3)


