"""
Geocoding Service using Nominatim API
"""
import asyncio
from typing import Optional

import httpx
import structlog

from shared.common.constants import CacheTTL
from shared.gps.schemas import GeocodingResult, ReverseGeocodingResult
from shared.redis_client import RedisClient, get_redis_client

logger = structlog.get_logger()


class NominatimClient:
    """Nominatim API client for geocoding operations"""

    def __init__(
        self,
        base_url: str = "https://nominatim.openstreetmap.org",
        user_agent: str = "ClinicHomeVisitSystem/1.0",
        rate_limit: float = 1.0,
    ):
        self.base_url = base_url
        self.user_agent = user_agent
        self.rate_limit = rate_limit
        self._redis: Optional[RedisClient] = None
        self._last_request_time: float = 0.0

    def set_redis(self, redis_client: RedisClient) -> None:
        """Set Redis client for caching"""
        self._redis = redis_client

    async def _rate_limit(self) -> None:
        """Apply rate limiting (1 request per second per Nominatim policy)"""
        if self._last_request_time > 0:
            elapsed = asyncio.get_event_loop().time() - self._last_request_time
            if elapsed < self.rate_limit:
                await asyncio.sleep(self.rate_limit - elapsed)
        self._last_request_time = asyncio.get_event_loop().time()

    async def _request(
        self,
        params: dict,
        endpoint: str = "search",
    ) -> Optional[dict]:
        """Make request to Nominatim API"""
        await self._rate_limit()

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }

        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error("nominatim_error", status=e.response.status_code)
                return None
            except Exception as e:
                logger.error("nominatim_error", error=str(e))
                return None

    async def geocode(
        self,
        address: str,
        country_codes: str = "vn",
        limit: int = 1,
    ) -> Optional[GeocodingResult]:
        """
        Convert address string to GPS coordinates.

        Args:
            address: Full address string (e.g., "123 Nguyen Trai, Ho Chi Minh")
            country_codes: Country code filter (default: vn for Vietnam)
            limit: Maximum number of results

        Returns:
            GeocodingResult with lat/lng or None if not found
        """
        cache_key = f"geocoding:{address}"
        if self._redis:
            cached = await self._redis.get_json(cache_key)
            if cached:
                logger.debug("geocoding_cache_hit", address=address)
                return GeocodingResult(**cached)

        params = {
            "q": address,
            "format": "json",
            "addressdetails": 1,
            "countrycodes": country_codes,
            "limit": limit,
        }

        results = await self._request(params)
        if results and len(results) > 0:
            result = results[0]
            geocoding = GeocodingResult(
                address=address,
                lat=float(result["lat"]),
                lng=float(result["lon"]),
                display_name=result.get("display_name", ""),
                type=result.get("type"),
                importance=result.get("importance"),
            )

            if self._redis:
                await self._redis.set_json(cache_key, geocoding.model_dump(), ttl=CacheTTL.GEOCODING)

            return geocoding

        return None

    async def reverse_geocode(
        self,
        lat: float,
        lng: float,
        zoom: int = 18,
    ) -> Optional[ReverseGeocodingResult]:
        """
        Convert GPS coordinates to address string.

        Args:
            lat: Latitude
            lng: Longitude
            zoom: Level of detail (0-18, higher = more detail)

        Returns:
            ReverseGeocodingResult with address or None if not found
        """
        cache_key = f"reverse_geocoding:{lat:.6f},{lng:.6f}"
        if self._redis:
            cached = await self._redis.get_json(cache_key)
            if cached:
                logger.debug("reverse_geocoding_cache_hit", lat=lat, lng=lng)
                return ReverseGeocodingResult(**cached)

        params = {
            "lat": lat,
            "lon": lng,
            "format": "json",
            "addressdetails": 1,
            "zoom": zoom,
        }

        result = await self._request(params, endpoint="reverse")
        if result:
            reverse = ReverseGeocodingResult(
                lat=lat,
                lng=lng,
                display_name=result.get("display_name", ""),
                address=result.get("address"),
            )

            if self._redis:
                await self._redis.set_json(
                    cache_key, reverse.model_dump(), ttl=CacheTTL.GEOCODING
                )

            return reverse

        return None


class GeocodingService:
    """High-level geocoding service with caching and fallback"""

    def __init__(
        self,
        nominatim_client: Optional[NominatimClient] = None,
        redis_client: Optional[RedisClient] = None,
    ):
        self.nominatim = nominatim_client or NominatimClient()
        if redis_client:
            self.nominatim.set_redis(redis_client)

    async def geocode_address(self, address: str) -> Optional[GeocodingResult]:
        """Geocode an address string"""
        return await self.nominatim.geocode(address)

    async def reverse_geocode(
        self, lat: float, lng: float
    ) -> Optional[ReverseGeocodingResult]:
        """Reverse geocode GPS coordinates"""
        return await self.nominatim.reverse_geocode(lat, lng)

    async def geocode_batch(
        self, addresses: list[str]
    ) -> dict[str, Optional[GeocodingResult]]:
        """Geocode multiple addresses concurrently"""
        tasks = [self.geocode_address(addr) for addr in addresses]
        results = await asyncio.gather(*tasks)
        return dict(zip(addresses, results))


# Convenience functions
async def geocode_address(
    address: str, redis_client: Optional[RedisClient] = None
) -> Optional[GeocodingResult]:
    """Convenience function for geocoding"""
    service = GeocodingService(redis_client=redis_client)
    return await service.geocode_address(address)


async def reverse_geocode(
    lat: float, lng: float, redis_client: Optional[RedisClient] = None
) -> Optional[ReverseGeocodingResult]:
    """Convenience function for reverse geocoding"""
    service = GeocodingService(redis_client=redis_client)
    return await service.reverse_geocode(lat, lng)
