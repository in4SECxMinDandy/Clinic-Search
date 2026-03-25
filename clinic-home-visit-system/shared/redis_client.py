"""
Redis Client for Caching and Pub/Sub
"""
import json
from typing import Any, Optional

import redis.asyncio as redis
from redis.asyncio import Redis

from shared.common.constants import CacheTTL


class RedisClient:
    """Redis client wrapper for async operations"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self._client: Optional[Redis] = None
        self._pubsub: Optional[redis.client.PubSub] = None

    async def connect(self) -> None:
        """Establish Redis connection"""
        self._client = redis.from_url(
            self.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def disconnect(self) -> None:
        """Close Redis connection"""
        if self._client:
            await self._client.close()

    @property
    def client(self) -> Redis:
        """Get Redis client"""
        if not self._client:
            raise RuntimeError("Redis client not connected. Call connect() first.")
        return self._client

    # ============ Caching Operations ============

    async def get(self, key: str) -> Optional[str]:
        """Get value by key"""
        return await self.client.get(key)

    async def get_json(self, key: str) -> Optional[dict[str, Any]]:
        """Get JSON value by key"""
        value = await self.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(
        self,
        key: str,
        value: str,
        ttl: Optional[int] = None,
    ) -> bool:
        """Set key-value with optional TTL"""
        return await self.client.set(key, value, ex=ttl)

    async def set_json(
        self,
        key: str,
        value: dict[str, Any],
        ttl: Optional[int] = None,
    ) -> bool:
        """Set JSON value with optional TTL"""
        return await self.set(key, json.dumps(value), ttl)

    async def delete(self, key: str) -> int:
        """Delete key"""
        return await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return await self.client.exists(key) > 0

    async def expire(self, key: str, ttl: int) -> bool:
        """Set TTL on key"""
        return await self.client.expire(key, ttl)

    async def ttl(self, key: str) -> int:
        """Get TTL of key"""
        return await self.client.ttl(key)

    # ============ Geo Operations ============

    async def geo_add(
        self,
        key: str,
        longitude: float,
        latitude: float,
        member: str,
    ) -> int:
        """Add member to geo set"""
        return await self.client.geoadd(key, (longitude, latitude, member))

    async def geo_search(
        self,
        key: str,
        longitude: float,
        latitude: float,
        radius_km: float,
        withdist: bool = True,
        withcoord: bool = True,
        count: Optional[int] = None,
        sort: str = "ASC",
    ) -> list[dict[str, Any]]:
        """Search for members within radius"""
        results = await self.client.geosearch(
            key,
            longitude=longitude,
            latitude=latitude,
            radius=radius_km,
            unit="km",
            withdist=withdist,
            withcoord=withcoord,
            count=count,
            sort=sort,
        )
        formatted = []
        for item in results:
            if withdist and withcoord:
                formatted.append(
                    {
                        "member": item[0],
                        "distance": float(item[1]),
                        "longitude": float(item[2][0]),
                        "latitude": float(item[2][1]),
                    }
                )
            elif withdist:
                formatted.append(
                    {
                        "member": item[0],
                        "distance": float(item[1]),
                    }
                )
            else:
                formatted.append({"member": item[0]})
        return formatted

    async def geo_distance(
        self,
        key: str,
        member1: str,
        member2: str,
        unit: str = "km",
    ) -> Optional[float]:
        """Get distance between two geo members"""
        distance = await self.client.geodist(key, member1, member2, unit)
        return float(distance) if distance else None

    # ============ Pub/Sub Operations ============

    async def publish(self, channel: str, message: str) -> int:
        """Publish message to channel"""
        return await self.client.publish(channel, message)

    async def publish_json(self, channel: str, data: dict[str, Any]) -> int:
        """Publish JSON message to channel"""
        return await self.publish(channel, json.dumps(data))

    async def subscribe(self, *channels: str) -> redis.client.PubSub:
        """Subscribe to channels"""
        pubsub = self.client.pubsub()
        await pubsub.subscribe(*channels)
        return pubsub

    async def psubscribe(self, *patterns: str) -> redis.client.PubSub:
        """Subscribe to channel patterns"""
        pubsub = self.client.pubsub()
        await pubsub.psubscribe(*patterns)
        return pubsub

    # ============ Rate Limiting ============

    async def rate_limit(
        self,
        key: str,
        limit: int,
        window_seconds: int,
    ) -> tuple[bool, int]:
        """
        Rate limiting using sliding window algorithm.
        Returns (is_allowed, remaining_requests)
        """
        current = await self.client.incr(key)
        if current == 1:
            await self.client.expire(key, window_seconds)
        remaining = max(0, limit - current)
        return current <= limit, remaining

    # ============ Cache Helpers ============

    async def cache_geocoding(
        self,
        address: str,
        result: dict[str, Any],
    ) -> None:
        """Cache geocoding result"""
        cache_key = f"geocoding:{address}"
        await self.set_json(cache_key, result, ttl=CacheTTL.GEOCODING)

    async def get_cached_geocoding(self, address: str) -> Optional[dict[str, Any]]:
        """Get cached geocoding result"""
        cache_key = f"geocoding:{address}"
        return await self.get_json(cache_key)

    async def cache_clinic_search(
        self,
        cache_key: str,
        results: list[dict[str, Any]],
    ) -> None:
        """Cache clinic search results"""
        await self.set_json(f"clinic_search:{cache_key}", results, ttl=CacheTTL.CLINIC_SEARCH)

    async def invalidate_clinic_cache(self) -> None:
        """Invalidate all clinic search caches"""
        keys = await self.client.keys("clinic_search:*")
        if keys:
            await self.client.delete(*keys)


# Global Redis client instance
redis_client: Optional[RedisClient] = None


def get_redis_client() -> RedisClient:
    """Get global Redis client instance"""
    global redis_client
    if redis_client is None:
        redis_url = "redis://localhost:6379"
        redis_client = RedisClient(redis_url)
    return redis_client


async def init_redis(redis_url: str = "redis://localhost:6379") -> RedisClient:
    """Initialize and connect Redis client"""
    global redis_client
    redis_client = RedisClient(redis_url)
    await redis_client.connect()
    return redis_client


async def close_redis() -> None:
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.disconnect()
        redis_client = None
