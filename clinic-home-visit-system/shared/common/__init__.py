"""
Shared Common Module
"""

from shared.common.exceptions import (
    AppException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    BusinessRuleViolation,
    RateLimitExceeded,
    ServiceUnavailableError,
    DuplicateResourceError,
    InvalidTokenError,
    AccountLockedError,
    SlotNotAvailableError,
    HomeVisitOutOfRangeError,
)
from shared.common.responses import (
    SuccessResponse,
    ErrorResponse,
    PaginatedResponse,
    HealthResponse,
    TokenResponse,
    MessageResponse,
)
from shared.common.constants import (
    UserRoles,
    BookingStatus,
    BookingType,
    PaymentMethod,
    PaymentStatus,
    NotificationStatus,
    NotificationTypes,
    NotificationChannels,
    EventChannels,
    DataSource,
    ReviewReportReason,
    ReviewReportStatus,
    CacheTTL,
    RateLimits,
)

__all__ = [
    # Exceptions
    "AppException",
    "ValidationError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "BusinessRuleViolation",
    "RateLimitExceeded",
    "ServiceUnavailableError",
    "DuplicateResourceError",
    "InvalidTokenError",
    "AccountLockedError",
    "SlotNotAvailableError",
    "HomeVisitOutOfRangeError",
    # Responses
    "SuccessResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "HealthResponse",
    "TokenResponse",
    "MessageResponse",
    # Constants
    "UserRoles",
    "BookingStatus",
    "BookingType",
    "PaymentMethod",
    "PaymentStatus",
    "NotificationStatus",
    "NotificationTypes",
    "NotificationChannels",
    "EventChannels",
    "DataSource",
    "ReviewReportReason",
    "ReviewReportStatus",
    "CacheTTL",
    "RateLimits",
]
