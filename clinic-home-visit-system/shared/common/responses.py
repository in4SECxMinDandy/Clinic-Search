"""
Standard API Response Models
"""
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response wrapper"""

    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    meta: Optional[dict[str, Any]] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """Standard error response"""

    success: bool = False
    error: str
    code: Optional[str] = None
    details: Optional[dict[str, Any]] = Field(default_factory=dict)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper"""

    success: bool = True
    data: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = "healthy"
    version: str
    service: str
    timestamp: str
    dependencies: Optional[dict[str, str]] = None


class TokenResponse(BaseModel):
    """JWT token response"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class MessageResponse(BaseModel):
    """Simple message response"""

    success: bool = True
    message: str
