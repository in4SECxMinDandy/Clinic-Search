"""
Message Broker for Event-Driven Communication
"""
import asyncio
import json
from typing import Any, Callable, Optional

import structlog

from shared.common.constants import EventChannels
from shared.redis_client import RedisClient, get_redis_client

logger = structlog.get_logger()


class EventPayload:
    """Event payload wrapper"""

    def __init__(
        self,
        event_type: str,
        data: dict[str, Any],
        correlation_id: Optional[str] = None,
        causation_id: Optional[str] = None,
    ):
        self.event_type = event_type
        self.data = data
        self.correlation_id = correlation_id
        self.causation_id = causation_id
        self.timestamp = asyncio.get_event_loop().time()

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "data": self.data,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EventPayload":
        return cls(
            event_type=data["event_type"],
            data=data["data"],
            correlation_id=data.get("correlation_id"),
            causation_id=data.get("causation_id"),
        )


class MessageBroker:
    """Event bus for inter-service communication via Redis Pub/Sub"""

    def __init__(self, redis_client: Optional[RedisClient] = None):
        self._redis = redis_client or get_redis_client()
        self._subscriptions: dict[str, asyncio.Task] = {}
        self._handlers: dict[str, list[Callable]] = {}

    async def publish(
        self,
        channel: str,
        payload: dict[str, Any],
        correlation_id: Optional[str] = None,
    ) -> int:
        """Publish event to channel"""
        event = EventPayload(
            event_type=channel,
            data=payload,
            correlation_id=correlation_id,
        )
        logger.info("event_published", channel=channel, correlation_id=correlation_id)
        return await self._redis.publish_json(channel, event.to_dict())

    async def subscribe(self, channel: str, handler: Callable) -> None:
        """Subscribe handler to channel"""
        if channel not in self._handlers:
            self._handlers[channel] = []
        self._handlers[channel].append(handler)

        if channel not in self._subscriptions:
            task = asyncio.create_task(self._listen(channel))
            self._subscriptions[channel] = task

    async def _listen(self, channel: str) -> None:
        """Listen for messages on channel"""
        pubsub = await self._redis.subscribe(channel)
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        event = EventPayload.from_dict(data)
                        for handler in self._handlers.get(channel, []):
                            await handler(event)
                    except json.JSONDecodeError as e:
                        logger.error("invalid_json", error=str(e), message=message)
        except asyncio.CancelledError:
            pass
        finally:
            await pubsub.unsubscribe(channel)

    async def publish_booking_created(
        self,
        booking_id: str,
        user_id: str,
        clinic_id: str,
        doctor_id: str,
        booking_type: str,
        scheduled_at: str,
    ) -> int:
        """Publish booking created event"""
        return await self.publish(
            EventChannels.BOOKING_CREATED,
            {
                "booking_id": booking_id,
                "user_id": user_id,
                "clinic_id": clinic_id,
                "doctor_id": doctor_id,
                "type": booking_type,
                "scheduled_at": scheduled_at,
            },
        )

    async def publish_booking_confirmed(
        self,
        booking_id: str,
        user_id: str,
        booking_type: str,
    ) -> int:
        """Publish booking confirmed event"""
        return await self.publish(
            EventChannels.BOOKING_CONFIRMED,
            {
                "booking_id": booking_id,
                "user_id": user_id,
                "type": booking_type,
            },
        )

    async def publish_booking_completed(
        self,
        booking_id: str,
        user_id: str,
        clinic_id: str,
    ) -> int:
        """Publish booking completed event"""
        return await self.publish(
            EventChannels.BOOKING_COMPLETED,
            {
                "booking_id": booking_id,
                "user_id": user_id,
                "clinic_id": clinic_id,
            },
        )

    async def publish_booking_cancelled(
        self,
        booking_id: str,
        user_id: str,
        reason: str,
    ) -> int:
        """Publish booking cancelled event"""
        return await self.publish(
            EventChannels.BOOKING_CANCELLED,
            {
                "booking_id": booking_id,
                "user_id": user_id,
                "reason": reason,
            },
        )

    async def publish_review_submitted(
        self,
        review_id: str,
        clinic_id: str,
        doctor_id: str,
        rating: int,
    ) -> int:
        """Publish review submitted event"""
        return await self.publish(
            EventChannels.REVIEW_SUBMITTED,
            {
                "review_id": review_id,
                "clinic_id": clinic_id,
                "doctor_id": doctor_id,
                "rating": rating,
            },
        )

    async def publish_crawl_completed(
        self,
        batch_id: str,
        stats: dict[str, Any],
    ) -> int:
        """Publish crawl completed event"""
        return await self.publish(
            EventChannels.CRAWL_COMPLETED,
            {
                "batch_id": batch_id,
                "stats": stats,
            },
        )

    async def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from channel"""
        if channel in self._subscriptions:
            self._subscriptions[channel].cancel()
            del self._subscriptions[channel]
        if channel in self._handlers:
            del self._handlers[channel]

    async def close(self) -> None:
        """Close all subscriptions"""
        for task in self._subscriptions.values():
            task.cancel()
        self._subscriptions.clear()
        self._handlers.clear()


# Global message broker instance
_message_broker: Optional[MessageBroker] = None


def get_message_broker() -> MessageBroker:
    """Get global message broker instance"""
    global _message_broker
    if _message_broker is None:
        _message_broker = MessageBroker()
    return _message_broker
