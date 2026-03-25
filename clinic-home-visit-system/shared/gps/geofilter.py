"""
Geofilter - Filter and Sort Points by Geographic Distance
"""
from typing import Callable, Optional, TypeVar

from shared.gps.haversine import calculate_haversine_distance, estimate_travel_time
from shared.gps.schemas import GPSCoordinates, NearbyResult

T = TypeVar("T")


def filter_by_radius(
    points: list[dict],
    center_lat: float,
    center_lng: float,
    radius_km: float,
    lat_field: str = "lat",
    lng_field: str = "lng",
) -> list[dict]:
    """
    Filter points within a given radius from center coordinates.

    Args:
        points: List of point dictionaries
        center_lat: Center latitude
        center_lng: Center longitude
        radius_km: Radius in kilometers
        lat_field: Name of latitude field in points
        lng_field: Name of longitude field in points

    Returns:
        Filtered list of points within radius
    """
    filtered = []
    for point in points:
        lat = point.get(lat_field)
        lng = point.get(lng_field)
        if lat is not None and lng is not None:
            distance = calculate_haversine_distance(center_lat, center_lng, lat, lng)
            if distance <= radius_km:
                point["_distance_km"] = distance
                filtered.append(point)
    return filtered


def find_nearby_points(
    points: list[dict],
    center_lat: float,
    center_lng: float,
    radius_km: float,
    limit: int = 10,
    lat_field: str = "lat",
    lng_field: str = "lng",
    id_field: str = "id",
    name_field: Optional[str] = None,
) -> list[NearbyResult]:
    """
    Find nearby points sorted by distance.

    Args:
        points: List of point dictionaries
        center_lat: Center latitude
        center_lng: Center longitude
        radius_km: Search radius in kilometers
        limit: Maximum number of results
        lat_field: Name of latitude field
        lng_field: Name of longitude field
        id_field: Name of ID field
        name_field: Optional name field

    Returns:
        List of NearbyResult sorted by distance
    """
    nearby = []

    for point in points:
        lat = point.get(lat_field)
        lng = point.get(lng_field)
        point_id = point.get(id_field)
        name = point.get(name_field) if name_field else None

        if lat is not None and lng is not None and point_id is not None:
            distance = calculate_haversine_distance(center_lat, center_lng, lat, lng)
            if distance <= radius_km:
                nearby.append(
                    NearbyResult(
                        id=str(point_id),
                        lat=lat,
                        lng=lng,
                        name=name,
                        distance_km=distance,
                        estimated_time_min=estimate_travel_time(distance, "driving"),
                    )
                )

    nearby.sort(key=lambda x: x.distance_km)
    return nearby[:limit]


def sort_by_distance(
    points: list[dict],
    center_lat: float,
    center_lng: float,
    lat_field: str = "lat",
    lng_field: str = "lng",
    descending: bool = False,
) -> list[dict]:
    """
    Sort points by distance from center.

    Args:
        points: List of point dictionaries
        center_lat: Center latitude
        center_lng: Center longitude
        lat_field: Name of latitude field
        lng_field: Name of longitude field
        descending: Sort descending if True

    Returns:
        Points sorted by distance
    """
    points_with_distance = []
    for point in points:
        lat = point.get(lat_field)
        lng = point.get(lng_field)
        if lat is not None and lng is not None:
            distance = calculate_haversine_distance(center_lat, center_lng, lat, lng)
            point_copy = point.copy()
            point_copy["_distance_km"] = distance
            points_with_distance.append(point_copy)

    points_with_distance.sort(key=lambda x: x["_distance_km"], reverse=descending)
    return points_with_distance


def calculate_centroid(points: list[GPSCoordinates]) -> GPSCoordinates:
    """
    Calculate the centroid (geometric center) of multiple GPS points.

    Args:
        points: List of GPSCoordinates

    Returns:
        Centroid coordinates
    """
    if not points:
        raise ValueError("Cannot calculate centroid of empty point list")

    if len(points) == 1:
        return points[0]

    total_lat = sum(p.lat for p in points)
    total_lng = sum(p.lng for p in points)
    count = len(points)

    return GPSCoordinates(
        lat=round(total_lat / count, 8),
        lng=round(total_lng / count, 8),
    )


def filter_by_bearing(
    points: list[dict],
    center_lat: float,
    center_lng: float,
    bearing_degrees: float,
    tolerance_degrees: float = 45.0,
    radius_km: Optional[float] = None,
    lat_field: str = "lat",
    lng_field: str = "lng",
) -> list[dict]:
    """
    Filter points within a bearing direction from center.

    Args:
        points: List of point dictionaries
        center_lat: Center latitude
        center_lng: Center longitude
        bearing_degrees: Target bearing (0-360)
        tolerance_degrees: Acceptable deviation from target bearing
        radius_km: Optional radius filter
        lat_field: Name of latitude field
        lng_field: Name of longitude field

    Returns:
        Filtered points within bearing and tolerance
    """
    from shared.gps.haversine import calculate_bearing

    filtered = []
    for point in points:
        lat = point.get(lat_field)
        lng = point.get(lng_field)
        if lat is not None and lng is not None:
            distance = calculate_haversine_distance(center_lat, center_lng, lat, lng)
            if radius_km and distance > radius_km:
                continue

            bearing = calculate_bearing(center_lat, center_lng, lat, lng)
            angle_diff = abs(bearing - bearing_degrees)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff

            if angle_diff <= tolerance_degrees:
                point_copy = point.copy()
                point_copy["_distance_km"] = distance
                point_copy["_bearing_degrees"] = bearing
                filtered.append(point_copy)

    return filtered
