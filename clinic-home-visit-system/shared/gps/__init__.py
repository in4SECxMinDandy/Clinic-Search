"""
GPS Module - Geographic Utilities
"""

from shared.gps.haversine import (
    calculate_haversine_distance,
    calculate_manhattan_distance,
    calculate_bearing,
    estimate_travel_time,
    calculate_distance_and_bearing,
    calculate_bounding_box,
    EARTH_RADIUS_KM,
    WALKING_SPEED_KMH,
    CYCLING_SPEED_KMH,
    DRIVING_SPEED_KMH,
)

from shared.gps.geocoding import (
    GeocodingService,
    NominatimClient,
    geocode_address,
    reverse_geocode,
)

from shared.gps.geofilter import (
    filter_by_radius,
    find_nearby_points,
    sort_by_distance,
    calculate_centroid,
    filter_by_bearing,
)

from shared.gps.routing import (
    OSRMRoutingService,
    get_route,
    get_directions,
    decode_polyline,
)

from shared.gps.schemas import (
    GPSCoordinates,
    DistanceResult,
    NearbyResult,
    RouteResult,
    RouteStep,
    GeocodingResult,
    ReverseGeocodingResult,
)

__all__ = [
    # Haversine
    "calculate_haversine_distance",
    "calculate_manhattan_distance",
    "calculate_bearing",
    "estimate_travel_time",
    "calculate_distance_and_bearing",
    "calculate_bounding_box",
    "EARTH_RADIUS_KM",
    "WALKING_SPEED_KMH",
    "CYCLING_SPEED_KMH",
    "DRIVING_SPEED_KMH",
    # Geocoding
    "GeocodingService",
    "NominatimClient",
    "geocode_address",
    "reverse_geocode",
    # Geofilter
    "filter_by_radius",
    "find_nearby_points",
    "sort_by_distance",
    "calculate_centroid",
    "filter_by_bearing",
    # Routing
    "OSRMRoutingService",
    "get_route",
    "get_directions",
    "decode_polyline",
    # Schemas
    "GPSCoordinates",
    "DistanceResult",
    "NearbyResult",
    "RouteResult",
    "RouteStep",
    "GeocodingResult",
    "ReverseGeocodingResult",
]
