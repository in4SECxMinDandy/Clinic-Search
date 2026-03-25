"""
System Constants and Enums
"""
from enum import Enum


class UserRoles(str, Enum):
    """User roles in the system"""

    ADMIN = "admin"
    PATIENT = "patient"
    DOCTOR = "doctor"
    CLINIC_OWNER = "clinic_owner"


class BookingStatus(str, Enum):
    """Booking status values"""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class BookingType(str, Enum):
    """Type of booking"""

    AT_CLINIC = "at_clinic"
    HOME_VISIT = "home_visit"


class PaymentMethod(str, Enum):
    """Payment methods"""

    CASH = "cash"
    TRANSFER = "transfer"
    VNPAY = "vnpay"
    MOMO = "momo"


class PaymentStatus(str, Enum):
    """Payment status"""

    UNPAID = "unpaid"
    PAID = "paid"
    REFUNDED = "refunded"


class NotificationStatus(str, Enum):
    """Notification delivery status"""

    PENDING = "pending"
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"


class NotificationTypes(str, Enum):
    """Types of notifications"""

    BOOKING_CREATED = "booking_created"
    BOOKING_CONFIRMED = "booking_confirmed"
    BOOKING_REMINDER_24H = "booking_reminder_24h"
    BOOKING_REMINDER_2H = "booking_reminder_2h"
    BOOKING_CANCELLED = "booking_cancelled"
    BOOKING_COMPLETED = "booking_completed"
    REVIEW_SUBMITTED = "review_submitted"
    REVIEW_REPLIED = "review_replied"
    PASSWORD_CHANGED = "password_changed"
    EMAIL_VERIFICATION = "email_verification"


class NotificationChannels(str, Enum):
    """Notification delivery channels"""

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class EventChannels:
    """Redis Pub/Sub event channels"""

    # Booking events
    BOOKING_CREATED = "event:booking:created"
    BOOKING_CONFIRMED = "event:booking:confirmed"
    BOOKING_COMPLETED = "event:booking:completed"
    BOOKING_CANCELLED = "event:booking:cancelled"
    BOOKING_EXPIRED = "event:booking:expired"

    # Review events
    REVIEW_SUBMITTED = "event:review:submitted"
    REVIEW_REPLIED = "event:review:replied"

    # Crawl events
    CRAWL_COMPLETED = "event:crawl:completed"
    GEOCODING_COMPLETED = "event:geocoding:completed"

    # Notification events
    NOTIFICATION_REQUESTED = "event:notification:requested"

    @classmethod
    def all(cls) -> list[str]:
        """Get all event channels"""
        return [
            cls.BOOKING_CREATED,
            cls.BOOKING_CONFIRMED,
            cls.BOOKING_COMPLETED,
            cls.BOOKING_CANCELLED,
            cls.BOOKING_EXPIRED,
            cls.REVIEW_SUBMITTED,
            cls.REVIEW_REPLIED,
            cls.CRAWL_COMPLETED,
            cls.GEOCODING_COMPLETED,
            cls.NOTIFICATION_REQUESTED,
        ]


class DataSource(str, Enum):
    """Data source for clinics"""

    MANUAL = "manual"
    CRAWLED = "crawled"


class ReviewReportReason(str, Enum):
    """Reasons for reporting a review"""

    SPAM = "spam"
    HARASSMENT = "harassment"
    INAPPROPRIATE = "inappropriate"
    FALSE_INFO = "false_information"
    OTHER = "other"


class ReviewReportStatus(str, Enum):
    """Status of a review report"""

    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


# Cache TTL constants (in seconds)
class CacheTTL:
    """Cache TTL values"""

    GEOCODING = 86400  # 24 hours
    CLINIC_SEARCH = 300  # 5 minutes
    USER_SESSION = 3600  # 1 hour
    OTP = 300  # 5 minutes


# Rate limiting
class RateLimits:
    """Rate limiting constants"""

    GEOCODING_PER_SECOND = 1
    SMS_PER_HOUR = 100
    EMAIL_PER_HOUR = 1000
    API_REQUESTS_PER_MINUTE = 60
