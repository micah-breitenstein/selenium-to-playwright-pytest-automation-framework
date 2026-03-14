from __future__ import annotations

import pytest

from tests.internet.geospatial import (
    coordinates_in_valid_range,
    haversine_km,
    is_within_radius_km,
    parse_coordinate,
)


def test_parse_coordinate_trims_and_parses_float() -> None:
    assert parse_coordinate(" 37.7749 ") == pytest.approx(37.7749)


def test_haversine_returns_zero_for_same_point() -> None:
    assert haversine_km(37.7749, -122.4194, 37.7749, -122.4194) == pytest.approx(0.0)


def test_haversine_is_symmetric() -> None:
    one_way = haversine_km(37.7749, -122.4194, 40.7128, -74.0060)
    other_way = haversine_km(40.7128, -74.0060, 37.7749, -122.4194)
    assert one_way == pytest.approx(other_way)


def test_is_within_radius_km() -> None:
    assert is_within_radius_km(37.7749, -122.4194, 37.7750, -122.4195, radius_km=1.0)


def test_coordinates_in_valid_range() -> None:
    assert coordinates_in_valid_range(0.0, 0.0)
    assert not coordinates_in_valid_range(91.0, 0.0)
    assert not coordinates_in_valid_range(0.0, 181.0)
