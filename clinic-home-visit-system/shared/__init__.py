"""
GPS & Location Utilities for Clinic Home Visit System

Provides:
- Haversine distance calculation
- Manhattan distance
- Geocoding via Nominatim
- Reverse geocoding
- Geofilter (points within radius)
- OSRM routing (shortest path)
"""

from shared.gps.haversine import (
    calculate_haversine_distance,
    calculate_manhattan_distance,
    calculate_bearing,
    estimate_travel_time,
    EARTH_RADIUS_KM,
)
from shared.gps.geocoding import (
    GeocodingService,
    NominatimClient,
    reverse_geocode,
    geocode_address,
)
from shared.gps.geofilter import (
    filter_by_radius,
    find_nearby_points,
    sort_by_distance,
    calculate_centroid,
)
from shared.gps.routing import (
    OSRMRoutingService,
    get_route,
    get_directions,
)
from shared.gps.schemas import (
    GPSCoordinates,
    DistanceResult,
    NearbyResult,
    RouteResult,
    GeocodingResult,
)

__all__ = [
    # Haversine
    "calculate_haversine_distance",
    "calculate_manhattan_distance",
    "calculate_bearing",
    "estimate_travel_time",
    "EARTH_RADIUS_KM",
    # Geocoding
    "GeocodingService",
    "NominatimClient",
    "reverse_geocode",
    "geocode_address",
    # Geofilter
    "filter_by_radius",
    "find_nearby_points",
    "sort_by_distance",
    "calculate_centroid",
    # Routing
    "OSRMRoutingService",
    "get_route",
    "get_directions",
    # Schemas
    "GPSCoordinates",
    "DistanceResult",
    "NearbyResult",
    "RouteResult",
    "GeocodingResult",
]
