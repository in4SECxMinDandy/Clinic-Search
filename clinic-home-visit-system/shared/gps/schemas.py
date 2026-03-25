"""
GPS Coordinate and Distance Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class GPSCoordinates(BaseModel):
    """GPS coordinate representation"""

    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")

    def to_tuple(self) -> tuple[float, float]:
        """Convert to (lat, lng) tuple"""
        return (self.lat, self.lng)


class DistanceResult(BaseModel):
    """Distance calculation result"""

    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float
    distance_km: float = Field(..., ge=0, description="Distance in kilometers")
    bearing_degrees: Optional[float] = Field(None, description="Initial bearing in degrees")


class NearbyResult(BaseModel):
    """Nearby point result"""

    id: str
    lat: float
    lng: float
    name: Optional[str] = None
    distance_km: float = Field(..., ge=0)
    estimated_time_min: Optional[float] = None


class RouteStep(BaseModel):
    """Route step/segment"""

    instruction: str
    distance_km: float
    duration_min: float
    start_lat: float
    start_lng: float
    end_lat: float
    end_lng: float


class RouteResult(BaseModel):
    """Routing result with shortest path"""

    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float
    distance_km: float
    duration_min: float
    geometry: Optional[str] = Field(None, description="Polyline encoded route")
    steps: list[RouteStep] = Field(default_factory=list)
    waypoints: Optional[list[GPSCoordinates]] = None


class GeocodingResult(BaseModel):
    """Geocoding result"""

    address: str
    lat: float
    lng: float
    display_name: str
    type: Optional[str] = None
    importance: Optional[float] = None


class ReverseGeocodingResult(BaseModel):
    """Reverse geocoding result"""

    lat: float
    lng: float
    display_name: str
    address: Optional[dict[str, str]] = None
