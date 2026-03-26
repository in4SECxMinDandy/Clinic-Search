"""
Clinic Service - GPS Router (Shared Endpoints)
"""
from typing import Optional, Union
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel

from shared.gps.haversine import (
    calculate_haversine_distance,
    calculate_manhattan_distance,
    calculate_bearing,
    estimate_travel_time,
)
from shared.gps.geocoding import NominatimClient, geocode_address, reverse_geocode
from shared.gps.routing import OSRMRoutingService, get_route
from shared.gps.geofilter import filter_by_radius
from clinic_service.utils.dependencies import get_db, get_redis

router = APIRouter()


class DistanceResponse(BaseModel):
    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float
    haversine_km: float
    manhattan_km: float
    bearing_degrees: float


class GeocodeResponse(BaseModel):
    address: str
    lat: float
    lng: float
    display_name: str


class ReverseGeocodeResponse(BaseModel):
    lat: float
    lng: float
    display_name: str
    address: Optional[dict] = None


class RouteResponse(BaseModel):
    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float
    distance_km: float
    duration_min: float
    geometry: Optional[str] = None
    steps: list


@router.get("/distance", response_model=DistanceResponse)
async def calculate_distance(
    from_lat: float = Query(..., ge=-90, le=90),
    from_lng: float = Query(..., ge=-180, le=180),
    to_lat: float = Query(..., ge=-90, le=90),
    to_lng: float = Query(..., ge=-180, le=180),
):
    """Calculate distance between two GPS points"""
    haversine = calculate_haversine_distance(from_lat, from_lng, to_lat, to_lng)
    manhattan = calculate_manhattan_distance(from_lat, from_lng, to_lat, to_lng)
    bearing = calculate_bearing(from_lat, from_lng, to_lat, to_lng)

    return DistanceResponse(
        from_lat=from_lat,
        from_lng=from_lng,
        to_lat=to_lat,
        to_lng=to_lng,
        haversine_km=haversine,
        manhattan_km=manhattan,
        bearing_degrees=bearing,
    )


@router.get("/geocode", response_model=GeocodeResponse)
async def geocode(
    address: str = Query(..., description="Address to geocode"),
):
    """Convert address to GPS coordinates using Nominatim"""
    result = await geocode_address(address)
    if not result:
        raise HTTPException(status_code=404, detail="Address not found")

    return GeocodeResponse(
        address=address,
        lat=result.lat,
        lng=result.lng,
        display_name=result.display_name,
    )


@router.get("/reverse", response_model=ReverseGeocodeResponse)
async def reverse_geocode_endpoint(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
):
    """Convert GPS coordinates to address"""
    result = await reverse_geocode(lat, lng)
    if not result:
        raise HTTPException(status_code=404, detail="Location not found")

    return ReverseGeocodeResponse(
        lat=lat,
        lng=lng,
        display_name=result.display_name,
        address=result.address,
    )


@router.get("/nearby")
async def find_nearby(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(default=10.0, ge=0.5, le=50),
):
    """Find all points within a radius (utility endpoint)"""
    return {
        "center_lat": lat,
        "center_lng": lng,
        "radius_km": radius_km,
        "note": "Use /clinics/nearby for clinics within radius",
    }


@router.get("/eta")
async def estimate_arrival(
    from_lat: float = Query(..., ge=-90, le=90),
    from_lng: float = Query(..., ge=-180, le=180),
    to_lat: float = Query(..., ge=-90, le=90),
    to_lng: float = Query(..., ge=-180, le=180),
    mode: str = Query(default="driving", regex="^(walking|cycling|driving)$"),
):
    """Estimate travel time between two points"""
    haversine = calculate_haversine_distance(from_lat, from_lng, to_lat, to_lng)
    travel_time = estimate_travel_time(haversine, mode)

    return {
        "from_lat": from_lat,
        "from_lng": from_lng,
        "to_lat": to_lat,
        "to_lng": to_lng,
        "straight_line_distance_km": haversine,
        "mode": mode,
        "estimated_time_min": travel_time,
    }


@router.get("/directions", response_model=RouteResponse)
async def get_directions(
    from_lat: float = Query(..., ge=-90, le=90),
    from_lng: float = Query(..., ge=-180, le=180),
    to_lat: float = Query(..., ge=-90, le=90),
    to_lng: float = Query(..., ge=-180, le=180),
    mode: str = Query(default="driving", regex="^(walking|cycling|driving)$"),
):
    """Get shortest path directions using OSRM"""
    result = await get_route(from_lat, from_lng, to_lat, to_lng, mode)

    if not result:
        return {
            "error": "No route found",
            "from_lat": from_lat,
            "from_lng": from_lng,
            "to_lat": to_lat,
            "to_lng": to_lng,
        }

    return RouteResponse(
        from_lat=from_lat,
        from_lng=from_lng,
        to_lat=to_lat,
        to_lng=to_lng,
        distance_km=result.distance_km,
        duration_min=result.duration_min,
        geometry=result.geometry,
        steps=[s.model_dump() for s in result.steps],
    )
