"""
Custom Exceptions for Clinic Home Visit System
"""

from typing import Any, Optional


class AppException(Exception):
    """Base exception for all application exceptions"""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": self.message,
            "status_code": self.status_code,
            "details": self.details,
        }


class ValidationError(AppException):
    """Raised when input validation fails"""

    def __init__(
        self, message: str = "Validation error", details: Optional[dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=422, details=details)


class AuthenticationError(AppException):
    """Raised when authentication fails"""

    def __init__(
        self, message: str = "Authentication failed", details: Optional[dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=401, details=details)


class AuthorizationError(AppException):
    """Raised when user doesn't have permission"""

    def __init__(
        self, message: str = "Permission denied", details: Optional[dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=403, details=details)


class NotFoundError(AppException):
    """Raised when resource is not found"""

    def __init__(
        self, message: str = "Resource not found", details: Optional[dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=404, details=details)


class BusinessRuleViolation(AppException):
    """Raised when a business rule is violated"""

    def __init__(
        self,
        message: str = "Business rule violation",
        details: Optional[dict[str, Any]] = None,
    ):
        super().__init__(message=message, status_code=400, details=details)


class RateLimitExceeded(AppException):
    """Raised when rate limit is exceeded"""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int = 60,
        details: Optional[dict[str, Any]] = None,
    ):
        details = details or {}
        details["retry_after"] = retry_after
        super().__init__(message=message, status_code=429, details=details)


class ServiceUnavailableError(AppException):
    """Raised when a dependent service is unavailable"""

    def __init__(
        self,
        service_name: str,
        message: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        msg = message or f"Service {service_name} is unavailable"
        super().__init__(message=msg, status_code=503, details=details)


class DuplicateResourceError(AppException):
    """Raised when trying to create a duplicate resource"""

    def __init__(
        self,
        resource_type: str,
        identifier: str,
        message: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        msg = message or f"{resource_type} with identifier '{identifier}' already exists"
        super().__init__(message=msg, status_code=409, details=details)


class InvalidTokenError(AuthenticationError):
    """Raised when token is invalid or expired"""

    def __init__(
        self, message: str = "Invalid or expired token", details: Optional[dict[str, Any]] = None
    ):
        super().__init__(message=message, details=details)


class AccountLockedError(AuthenticationError):
    """Raised when account is locked due to too many failed attempts"""

    def __init__(
        self,
        locked_until: str,
        message: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        details = details or {}
        details["locked_until"] = locked_until
        msg = message or "Account is temporarily locked due to too many failed login attempts"
        super().__init__(message=msg, details=details)


class SlotNotAvailableError(BusinessRuleViolation):
    """Raised when booking slot is not available"""

    def __init__(
        self,
        doctor_id: str,
        slot_time: str,
        message: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        details = details or {}
        details["doctor_id"] = doctor_id
        details["slot_time"] = slot_time
        msg = message or f"Slot at {slot_time} is not available for this doctor"
        super().__init__(message=msg, details=details)


class HomeVisitOutOfRangeError(BusinessRuleViolation):
    """Raised when home visit location is out of doctor's service range"""

    def __init__(
        self,
        doctor_id: str,
        distance_km: float,
        max_radius_km: float,
        message: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        details = details or {}
        details["distance_km"] = distance_km
        details["max_radius_km"] = max_radius_km
        msg = (
            message
            or f"Location is {distance_km}km away, exceeds doctor's {max_radius_km}km service range"
        )
        super().__init__(message=msg, details=details)
