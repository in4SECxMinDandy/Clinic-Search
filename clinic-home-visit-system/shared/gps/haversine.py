"""
Haversine Distance and Navigation Calculations
"""
import math
from typing import Optional

from shared.gps.schemas import DistanceResult

EARTH_RADIUS_KM = 6371.0
EARTH_RADIUS_M = 6371000.0

WALKING_SPEED_KMH = 5.0
CYCLING_SPEED_KMH = 15.0
DRIVING_SPEED_KMH = 40.0  # Urban average


def calculate_haversine_distance(
    lat1: float,
    lng1: float,
    lat2: float,
    lng2: float,
    radius_km: float = EARTH_RADIUS_KM,
) -> float:
    """
    Calculate the great-circle distance between two points using Haversine formula.

    Args:
        lat1: Latitude of point 1
        lng1: Longitude of point 1
        lat2: Latitude of point 2
        lng2: Longitude of point 2
        radius_km: Earth radius in km (default 6371)

    Returns:
        Distance in kilometers
    """
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = radius_km * c
    return round(distance, 3)


def calculate_manhattan_distance(
    lat1: float,
    lng1: float,
    lat2: float,
    lng2: float,
) -> float:
    """
    Calculate Manhattan distance (suitable for urban grid layouts).

    Args:
        lat1: Latitude of point 1
        lng1: Longitude of point 1
        lat2: Latitude of point 2
        lng2: Longitude of point 2

    Returns:
        Approximate distance in kilometers for grid-based movement
    """
    lat_diff_km = abs(lat2 - lat1) * 111.0
    lng_diff_km = abs(lng2 - lng1) * 111.0 * math.cos(math.radians((lat1 + lat2) / 2))
    return round(abs(lat_diff_km) + abs(lng_diff_km), 3)


def calculate_bearing(
    lat1: float,
    lng1: float,
    lat2: float,
    lng2: float,
) -> float:
    """
    Calculate the initial bearing (forward azimuth) from point 1 to point 2.

    Args:
        lat1: Latitude of point 1
        lng1: Longitude of point 1
        lat2: Latitude of point 2
        lng2: Longitude of point 2

    Returns:
        Bearing in degrees (0-360)
    """
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lng = math.radians(lng2 - lng1)

    x = math.sin(delta_lng) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(
        lat2_rad
    ) * math.cos(delta_lng)

    initial_bearing = math.atan2(x, y)
    bearing = (math.degrees(initial_bearing) + 360) % 360
    return round(bearing, 1)


def estimate_travel_time(
    distance_km: float,
    mode: str = "walking",
    walking_speed_kmh: float = WALKING_SPEED_KMH,
    cycling_speed_kmh: float = CYCLING_SPEED_KMH,
    driving_speed_kmh: float = DRIVING_SPEED_KMH,
) -> float:
    """
    Estimate travel time based on distance and mode of transport.

    Args:
        distance_km: Distance in kilometers
        mode: Transport mode (walking, cycling, driving)
        walking_speed_kmh: Walking speed (default 5 km/h)
        cycling_speed_kmh: Cycling speed (default 15 km/h)
        driving_speed_kmh: Driving speed (default 40 km/h, urban average)

    Returns:
        Estimated travel time in minutes
    """
    speeds = {
        "walking": walking_speed_kmh,
        "cycling": cycling_speed_kmh,
        "driving": driving_speed_kmh,
    }
    speed = speeds.get(mode.lower(), WALKING_SPEED_KMH)
    hours = distance_km / speed
    minutes = hours * 60
    return round(minutes, 1)


def calculate_distance_and_bearing(
    lat1: float,
    lng1: float,
    lat2: float,
    lng2: float,
) -> DistanceResult:
    """Calculate both distance and bearing between two points."""
    distance = calculate_haversine_distance(lat1, lng1, lat2, lng2)
    bearing = calculate_bearing(lat1, lng1, lat2, lng2)
    return DistanceResult(
        from_lat=lat1,
        from_lng=lng1,
        to_lat=lat2,
        to_lng=lng2,
        distance_km=distance,
        bearing_degrees=bearing,
    )


def calculate_bounding_box(
    lat: float,
    lng: float,
    radius_km: float,
) -> tuple[float, float, float, float]:
    """
    Calculate bounding box coordinates for a given center and radius.

    Returns:
        (min_lat, max_lat, min_lng, max_lng)
    """
    lat_delta = radius_km / 111.0
    lng_delta = radius_km / (111.0 * math.cos(math.radians(lat)))
    return (
        lat - lat_delta,
        lat + lat_delta,
        lng - lng_delta,
        lng + lng_delta,
    )
