"""
OSRM Routing Service - Shortest Path Calculation
"""
from typing import Optional

import httpx
import structlog

from shared.gps.schemas import GPSCoordinates, RouteResult, RouteStep

logger = structlog.get_logger()


class OSRMRoutingService:
    """
    OSRM (Open Source Routing Machine) client for shortest path routing.
    Uses the free OSRM demo server or self-hosted instance.

    Features:
    - Shortest path between two points
    - Turn-by-turn directions
    - Route geometry (polyline)
    - Distance and duration estimation
    """

    def __init__(
        self,
        base_url: str = "https://router.project-osrm.org",
        timeout: float = 30.0,
    ):
        self.base_url = base_url
        self.timeout = timeout

    async def get_route(
        self,
        from_lat: float,
        from_lng: float,
        to_lat: float,
        to_lng: float,
        mode: str = "driving",
        alternatives: int = 0,
    ) -> Optional[RouteResult]:
        """
        Get shortest path route between two points.

        Args:
            from_lat: Start latitude
            from_lng: Start longitude
            to_lat: End latitude
            to_lng: End longitude
            mode: Transportation mode (driving, walking, cycling)
            alternatives: Number of alternative routes (0-3)

        Returns:
            RouteResult with distance, duration, geometry, and steps
        """
        url = f"{self.base_url}/route/v1/{mode}/{from_lng},{from_lat};{to_lng},{to_lat}"
        params = {
            "overview": "full",
            "geometries": "polyline",
            "steps": "true",
            "alternatives": str(alternatives),
            "annotations": "false",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("code") != "Ok" or not data.get("routes"):
                    logger.warning("osrm_no_route", code=data.get("code"))
                    return None

                route = data["routes"][0]
                steps = self._parse_steps(route.get("legs", [{}])[0].get("steps", []))

                return RouteResult(
                    from_lat=from_lat,
                    from_lng=from_lng,
                    to_lat=to_lat,
                    to_lng=to_lng,
                    distance_km=route["distance"] / 1000,
                    duration_min=route["duration"] / 60,
                    geometry=route.get("geometry"),
                    steps=steps,
                )

            except httpx.HTTPStatusError as e:
                logger.error("osrm_http_error", status=e.response.status_code)
                return None
            except Exception as e:
                logger.error("osrm_error", error=str(e))
                return None

    def _parse_steps(self, raw_steps: list[dict]) -> list[RouteStep]:
        """Parse raw OSRM steps into RouteStep objects"""
        steps = []
        for step in raw_steps:
            maneuver = step.get("maneuver", {})
            location = maneuver.get("location", [])

            steps.append(
                RouteStep(
                    instruction=step.get("maneuver", {}).get("instruction", ""),
                    distance_km=step.get("distance", 0) / 1000,
                    duration_min=step.get("duration", 0) / 60,
                    start_lat=location[1] if len(location) > 1 else 0,
                    start_lng=location[0] if len(location) > 0 else 0,
                    end_lat=step.get("way_points", [0, 0])[1],
                    end_lng=step.get("way_points", [0, 0])[0],
                )
            )
        return steps

    async def get_route_geometry(
        self,
        waypoints: list[tuple[float, float]],
        mode: str = "driving",
    ) -> Optional[str]:
        """
        Get route geometry for multiple waypoints (via points).

        Args:
            waypoints: List of (lat, lng) tuples
            mode: Transportation mode

        Returns:
            Encoded polyline string
        """
        if len(waypoints) < 2:
            return None

        coords = ";".join(f"{lng},{lat}" for lat, lng in waypoints)
        url = f"{self.base_url}/route/v1/{mode}/{coords}"
        params = {
            "overview": "full",
            "geometries": "polyline",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("code") == "Ok" and data.get("routes"):
                    return data["routes"][0].get("geometry")
            except Exception:
                pass

        return None


async def get_route(
    from_lat: float,
    from_lng: float,
    to_lat: float,
    to_lng: float,
    mode: str = "driving",
) -> Optional[RouteResult]:
    """Convenience function to get shortest route"""
    service = OSRMRoutingService()
    return await service.get_route(from_lat, from_lng, to_lat, to_lng, mode)


async def get_directions(
    from_lat: float,
    from_lng: float,
    to_lat: float,
    to_lng: float,
    mode: str = "driving",
) -> Optional[RouteResult]:
    """Convenience function to get directions with steps"""
    return await get_route(from_lat, from_lng, to_lat, to_lng, mode)


def decode_polyline(encoded: str, precision: int = 5) -> list[GPSCoordinates]:
    """
    Decode Google-encoded polyline string to list of coordinates.

    Args:
        encoded: Encoded polyline string
        precision: Coordinate precision (default 5 for 5 decimal places)

    Returns:
        List of GPSCoordinates
    """
    index = 0
    lat = 0
    lng = 0
    coordinates = []
    factor = 10**precision

    while index < len(encoded):
        byte = ord(encoded[index]) - 63
        index += 1
        shift = 0
        result = 0

        while byte >= 0x20:
            result += (byte - 0x21) << shift
            shift += 5
            if index < len(encoded):
                byte = ord(encoded[index]) - 63
                index += 1

        dlat = result & 1
        result >>= 1
        if dlat:
            lat -= result
        else:
            lat += result

        shift = 0
        result = 0
        while index < len(encoded):
            byte = ord(encoded[index]) - 63
            index += 1
            if byte < 0x20:
                result += byte
                break
            result += (byte - 0x20) << shift
            shift += 5

        dlng = result & 1
        result >>= 1
        if dlng:
            lng -= result
        else:
            lng += result

        coordinates.append(
            GPSCoordinates(
                lat=lat / factor,
                lng=lng / factor,
            )
        )

    return coordinates
