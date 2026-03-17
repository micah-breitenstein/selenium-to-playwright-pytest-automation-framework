from __future__ import annotations

import json
import math
import os
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

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

USER_LATITUDE = 37.7786236
USER_LONGITUDE = -121.9416398
USE_MOCK_GEOLOCATION = os.getenv("PW_USE_MOCK_GEO", "1").lower() not in {
    "0",
    "false",
    "no",
}
PARK_SEARCH_RADIUS_M = int(os.getenv("PW_PARK_RADIUS_M", "3000"))
ADDRESS_SEARCH_RADIUS_M = int(os.getenv("PW_ADDRESS_RADIUS_M", "3000"))
TARGET_SEARCH_RADIUS_M = int(os.getenv("PW_TARGET_RADIUS_M", "20000"))
TARGET_MIN_RESULTS = int(os.getenv("PW_TARGET_MIN_RESULTS", "2"))
TARGET_QUERY_TIMEOUT_S = int(os.getenv("PW_TARGET_QUERY_TIMEOUT_S", "10"))
TARGET_HTTP_TIMEOUT_S = int(os.getenv("PW_TARGET_HTTP_TIMEOUT_S", "12"))
TARGET_PARK_TARGET_RADIUS_M = int(os.getenv("PW_TARGET_PARK_TARGET_RADIUS_M", "20000"))
TARGET_PARK_PARK_RADIUS_M = int(os.getenv("PW_TARGET_PARK_PARK_RADIUS_M", "5000"))
START_ADDRESS_OVERRIDE = os.getenv("PW_START_ADDRESS_OVERRIDE", "").strip()


def _element_coordinates(element: dict) -> tuple[float | None, float | None]:
    latitude = element.get("lat")
    longitude = element.get("lon")

    center = element.get("center", {})
    if latitude is None:
        latitude = center.get("lat")
    if longitude is None:
        longitude = center.get("lon")

    if latitude is None or longitude is None:
        return None, None

    return float(latitude), float(longitude)


def _place_record(
    name: str,
    origin_lat: float,
    origin_lon: float,
    place_lat: float,
    place_lon: float,
) -> dict:
    distance_km = haversine_km(origin_lat, origin_lon, place_lat, place_lon)
    return {
        "name": name,
        "latitude": place_lat,
        "longitude": place_lon,
        "distance_km": distance_km,
    }


def _closest_place(places: list[dict]) -> dict:
    return places[0]


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
        park_lat, park_lon = _element_coordinates(element)
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


def _targets_nearby(lat: float, lon: float, radius_m: int = 20000) -> list[dict]:
    query = f"""
    [out:json][timeout:{TARGET_QUERY_TIMEOUT_S}];
    (
      node["name"~"target", i](around:{radius_m},{lat},{lon});
      way["name"~"target", i](around:{radius_m},{lat},{lon});
      relation["name"~"target", i](around:{radius_m},{lat},{lon});
      node["brand"~"target", i](around:{radius_m},{lat},{lon});
      way["brand"~"target", i](around:{radius_m},{lat},{lon});
      relation["brand"~"target", i](around:{radius_m},{lat},{lon});
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
        with urlopen(request, timeout=TARGET_HTTP_TIMEOUT_S) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, OSError, json.JSONDecodeError):
        return []

    targets: list[dict] = []
    seen = set()
    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name", "Target")
        if "target" not in name.lower():
            continue

        store_lat, store_lon = _element_coordinates(element)
        if store_lat is None or store_lon is None:
            continue

        key = (name, store_lat, store_lon)
        if key in seen:
            continue
        seen.add(key)

        targets.append(
            _place_record(
                name=name,
                origin_lat=lat,
                origin_lon=lon,
                place_lat=store_lat,
                place_lon=store_lon,
            )
        )

    targets.sort(key=lambda store: store["distance_km"])
    return targets


def _targets_nearby_nominatim(
    lat: float, lon: float, radius_m: int = 20000, limit: int = 20
) -> list[dict]:
    lat_delta = radius_m / 111_320
    lon_delta = radius_m / (111_320 * max(0.1, math.cos(math.radians(lat))))
    left = lon - lon_delta
    right = lon + lon_delta
    top = lat + lat_delta
    bottom = lat - lat_delta

    params = urlencode(
        {
            "q": "Target",
            "format": "jsonv2",
            "limit": limit,
            "bounded": 1,
            "viewbox": f"{left},{top},{right},{bottom}",
            "addressdetails": 1,
        }
    )
    request = Request(
        f"https://nominatim.openstreetmap.org/search?{params}",
        headers={"User-Agent": "selenium-python-basics-geolocation-tests"},
    )

    try:
        with urlopen(request, timeout=TARGET_HTTP_TIMEOUT_S) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, OSError, json.JSONDecodeError):
        return []

    targets: list[dict] = []
    seen = set()
    for item in data:
        name = item.get("name") or item.get("display_name", "Target")
        if "target" not in str(name).lower():
            continue

        try:
            store_lat = float(item.get("lat"))
            store_lon = float(item.get("lon"))
        except (TypeError, ValueError):
            continue

        key = (str(name), store_lat, store_lon)
        if key in seen:
            continue
        seen.add(key)

        targets.append(
            _place_record(
                name=str(name),
                origin_lat=lat,
                origin_lon=lon,
                place_lat=store_lat,
                place_lon=store_lon,
            )
        )

    targets.sort(key=lambda store: store["distance_km"])
    return targets


def _targets_nearby_with_fallback(
    lat: float, lon: float, radius_m: int = 20000
) -> list[dict]:
    primary_results = _targets_nearby(lat, lon, radius_m=radius_m)
    if len(primary_results) >= 2:
        return primary_results

    fallback_results = _targets_nearby_nominatim(lat, lon, radius_m=radius_m)

    merged: list[dict] = []
    seen = set()
    for store in [*primary_results, *fallback_results]:
        key = (
            store["name"].lower(),
            round(float(store["latitude"]), 5),
            round(float(store["longitude"]), 5),
        )
        if key in seen:
            continue
        seen.add(key)
        merged.append(store)

    merged.sort(key=lambda store: store["distance_km"])
    return merged


def _reverse_geocode(latitude: float, longitude: float) -> dict:
    params = urlencode(
        {
            "format": "jsonv2",
            "lat": f"{latitude}",
            "lon": f"{longitude}",
            "addressdetails": 1,
            "zoom": 18,
        }
    )
    request = Request(
        f"https://nominatim.openstreetmap.org/reverse?{params}",
        headers={"User-Agent": "selenium-python-basics-geolocation-tests"},
    )

    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        pytest.skip(f"Reverse geocoding unavailable for park address lookup: {exc}")

    return payload


def _search_geocode(query: str) -> dict:
    params = urlencode(
        {
            "q": query,
            "format": "jsonv2",
            "limit": 1,
            "addressdetails": 1,
        }
    )
    request = Request(
        f"https://nominatim.openstreetmap.org/search?{params}",
        headers={"User-Agent": "selenium-python-basics-geolocation-tests"},
    )

    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        pytest.skip(f"Address search unavailable for override lookup: {exc}")

    if not payload:
        pytest.skip(f"No result found for PW_START_ADDRESS_OVERRIDE={query!r}")

    return payload[0]


def _nearest_address_tags(
    lat: float, lon: float, radius_m: int = ADDRESS_SEARCH_RADIUS_M
) -> dict[str, str]:
    query = f"""
    [out:json][timeout:25];
    (
      node["addr:housenumber"](around:{radius_m},{lat},{lon});
      way["addr:housenumber"](around:{radius_m},{lat},{lon});
      relation["addr:housenumber"](around:{radius_m},{lat},{lon});
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
    except (URLError, TimeoutError, OSError, json.JSONDecodeError):
        return {}

    best_tags: dict[str, str] = {}
    best_distance_km: float | None = None

    for element in data.get("elements", []):
        tags = element.get("tags", {})
        if not tags.get("addr:housenumber"):
            continue

        element_lat = element.get("lat")
        element_lon = element.get("lon")
        center = element.get("center", {})
        if element_lat is None:
            element_lat = center.get("lat")
        if element_lon is None:
            element_lon = center.get("lon")

        if element_lat is None or element_lon is None:
            continue

        distance_km = haversine_km(lat, lon, float(element_lat), float(element_lon))
        if best_distance_km is None or distance_km < best_distance_km:
            best_distance_km = distance_km
            best_tags = tags

    return best_tags


def _format_address_fields(
    geocode_payload: dict, nearest_tags: dict[str, str] | None = None
) -> dict[str, str]:
    address = geocode_payload.get("address", {})
    nearest_tags = nearest_tags or {}

    house_number = nearest_tags.get("addr:housenumber") or address.get("house_number")
    road_name = (
        nearest_tags.get("addr:street")
        or address.get("road")
        or address.get("pedestrian")
        or address.get("footway")
    )

    street_parts = [
        house_number,
        road_name,
    ]
    full_address = " ".join(part for part in street_parts if part)
    display_name = geocode_payload.get("display_name") or ""
    display_address1 = display_name.split(",", 1)[0].strip() if display_name else ""
    address1 = full_address or display_address1
    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("hamlet")
    )
    return {
        "address1": address1 or "N/A",
        "address": full_address or "N/A",
        "city": nearest_tags.get("addr:city") or city or "N/A",
        "state": nearest_tags.get("addr:state") or address.get("state") or "N/A",
        "county": address.get("county") or "N/A",
        "zipcode": nearest_tags.get("addr:postcode") or address.get("postcode") or "N/A",
    }


def _google_maps_search_url(latitude: float, longitude: float) -> str:
    return (
        "https://www.google.com/maps/search/?api=1&query="
        f"{latitude},{longitude}"
    )


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


def _navigate_route(pw_page, route_url: str, wait_ms: int) -> None:
    pw_page.goto(route_url, wait_until="domcontentloaded", timeout=60_000)
    if wait_ms > 0:
        pw_page.wait_for_timeout(wait_ms)


def _print_route_leg(label: str, destination: dict, route_url: str) -> None:
    print(f"{label}: {destination['name']} ({destination['distance_km']:.2f} km)")
    print(f"Route URL: {route_url}")


def _get_start_address() -> dict[str, str]:
    if START_ADDRESS_OVERRIDE:
        print(f"Using start address override: {START_ADDRESS_OVERRIDE}")
        return _format_address_fields(_search_geocode(START_ADDRESS_OVERRIDE))

    return _format_address_fields(
        _reverse_geocode(USER_LATITUDE, USER_LONGITUDE),
    )


def _print_starting_point_summary(start_address: dict[str, str]) -> None:
    print("\n=== Starting Point Summary ===")
    print(f"Address: {start_address['address1']}")
    print(f"City: {start_address['city']}")
    print(f"State: {start_address['state']}")
    print(f"County: {start_address['county']}")
    print(f"Zip: {start_address['zipcode']}")


def _print_closest_park_summary(parks: list[dict]) -> None:
    closest = parks[0]
    closest_maps_url = _google_maps_search_url(
        closest["latitude"], closest["longitude"]
    )
    closest_address = _format_address_fields(
        _reverse_geocode(closest["latitude"], closest["longitude"])
    )

    print("\n=== Closest Park Summary ===")
    print(
        f"Closest park: {closest['name']} ({closest['distance_km']:.2f} km)"
        f" | {closest_maps_url}"
    )
    print(f"Address: {closest_address['address1']}")
    print(f"City: {closest_address['city']}")
    print(f"State: {closest_address['state']}")
    print(f"County: {closest_address['county']}")
    print(f"Zip: {closest_address['zipcode']}")

    coyote_crossing = [
        park["name"] for park in parks if "coyote crossing" in park["name"].lower()
    ]
    if coyote_crossing:
        print(f"Likely match: {coyote_crossing[0]}")


def _print_target_primary_backup_summary(
    primary: dict,
    backup: dict,
    primary_route_url: str,
    backup_route_url: str,
) -> None:
    primary_maps_url = _google_maps_search_url(
        primary["latitude"], primary["longitude"]
    )
    backup_maps_url = _google_maps_search_url(backup["latitude"], backup["longitude"])

    print("\n=== Closest Target Summary ===")
    print(
        f"Primary: {primary['name']} ({primary['distance_km']:.2f} km)"
        f" | {primary_maps_url}"
    )
    print(f"Primary route: {primary_route_url}")
    print(
        f"Backup: {backup['name']} ({backup['distance_km']:.2f} km)"
        f" | {backup_maps_url}"
    )
    print(f"Backup route: {backup_route_url}")


def _print_target_stop_summary(target: dict, route_url: str) -> None:
    target_maps_url = _google_maps_search_url(target["latitude"], target["longitude"])

    print("\n=== Target Stop Summary ===")
    print(
        f"Target: {target['name']} ({target['distance_km']:.2f} km)"
        f" | {target_maps_url}"
    )
    print(f"Route: {route_url}")


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


@pytest.mark.playwright
def test_geolocation_logs_nearby_parks_for_user_coordinates_playwright(
    pw_mock_geolocation, pw_page, base_url
):
    if USE_MOCK_GEOLOCATION:
        pw_mock_geolocation(USER_LATITUDE, USER_LONGITUDE)
        print(f"Using mocked geolocation: ({USER_LATITUDE}, {USER_LONGITUDE})")
    else:
        # Playwright has no real GPS access; USE_MOCK_GEOLOCATION=0 means
        # skip the page interaction and use USER_LATITUDE/USER_LONGITUDE directly.
        print(
            f"Mock disabled — using USER_LATITUDE/USER_LONGITUDE directly: "
            f"({USER_LATITUDE}, {USER_LONGITUDE})"
        )

    page = PWGeolocationPage(pw_page, base_url=base_url).open()
    page.click_where_am_i().wait_for_coordinates()

    actual_lat = (
        parse_coordinate(page.lat_text()) if USE_MOCK_GEOLOCATION else USER_LATITUDE
    )
    actual_long = (
        parse_coordinate(page.long_text()) if USE_MOCK_GEOLOCATION else USER_LONGITUDE
    )

    parks = _parks_nearby(actual_lat, actual_long, radius_m=PARK_SEARCH_RADIUS_M)

    start_address = _get_start_address()

    assert parks, (
        f"No nearby parks found within {PARK_SEARCH_RADIUS_M}m of "
        f"({actual_lat}, {actual_long})"
    )

    print(f"Nearby parks for ({actual_lat}, {actual_long}):")
    for park in parks[:10]:
        maps_url = _google_maps_search_url(park["latitude"], park["longitude"])
        print(f" - {park['name']} ({park['distance_km']:.2f} km) | {maps_url}")

    _print_starting_point_summary(start_address)
    _print_closest_park_summary(parks)


@pytest.mark.playwright
def test_geolocation_navigates_google_maps_all_nearby_parks_playwright(
    pw_mock_geolocation, pw_page, base_url, pw_nav_wait_ms
):
    if USE_MOCK_GEOLOCATION:
        pw_mock_geolocation(USER_LATITUDE, USER_LONGITUDE)

    page = PWGeolocationPage(pw_page, base_url=base_url).open()
    page.click_where_am_i().wait_for_coordinates()

    actual_lat = (
        parse_coordinate(page.lat_text()) if USE_MOCK_GEOLOCATION else USER_LATITUDE
    )
    actual_long = (
        parse_coordinate(page.long_text()) if USE_MOCK_GEOLOCATION else USER_LONGITUDE
    )
    parks = _parks_nearby(actual_lat, actual_long, radius_m=PARK_SEARCH_RADIUS_M)

    if not parks:
        pytest.skip(f"No named parks found near ({actual_lat}, {actual_long})")

    parks_to_visit = parks[:10]

    start_address = _get_start_address()

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
        _navigate_route(pw_page, maps_url, pw_nav_wait_ms)

    _print_starting_point_summary(start_address)
    _print_closest_park_summary(parks)


@pytest.mark.playwright
def test_geolocation_navigates_to_closest_target_with_backup_playwright(
    pw_mock_geolocation, pw_page, base_url, pw_nav_wait_ms
):
    if USE_MOCK_GEOLOCATION:
        pw_mock_geolocation(USER_LATITUDE, USER_LONGITUDE)

    page = PWGeolocationPage(pw_page, base_url=base_url).open()
    page.click_where_am_i().wait_for_coordinates()

    actual_lat = (
        parse_coordinate(page.lat_text()) if USE_MOCK_GEOLOCATION else USER_LATITUDE
    )
    actual_long = (
        parse_coordinate(page.long_text()) if USE_MOCK_GEOLOCATION else USER_LONGITUDE
    )

    targets = _targets_nearby_with_fallback(
        actual_lat,
        actual_long,
        radius_m=TARGET_SEARCH_RADIUS_M,
    )
    if len(targets) < 2:
        pytest.skip(
            f"Found {len(targets)} Target locations within {TARGET_SEARCH_RADIUS_M}m; "
            "need at least 2 for primary + backup"
        )

    primary = targets[0]
    backup = targets[1]
    start_address = _get_start_address()

    primary_route_url = _google_maps_directions_url(
        actual_lat,
        actual_long,
        primary["latitude"],
        primary["longitude"],
    )
    backup_route_url = _google_maps_directions_url(
        actual_lat,
        actual_long,
        backup["latitude"],
        backup["longitude"],
    )

    print(
        f"Routing from ({actual_lat}, {actual_long}) to Target 1: "
        f"{primary['name']}"
    )
    print(f"Route URL: {primary_route_url}")
    _navigate_route(pw_page, primary_route_url, pw_nav_wait_ms)

    print(
        f"Routing from ({actual_lat}, {actual_long}) to Target 2: "
        f"{backup['name']}"
    )
    print(f"Route URL: {backup_route_url}")
    _navigate_route(pw_page, backup_route_url, pw_nav_wait_ms)

    _print_starting_point_summary(start_address)
    _print_target_primary_backup_summary(
        primary,
        backup,
        primary_route_url,
        backup_route_url,
    )
