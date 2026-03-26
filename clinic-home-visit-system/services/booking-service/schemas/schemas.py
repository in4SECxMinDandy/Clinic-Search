"""
Booking Service - Pydantic Schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class BookingCreate(BaseModel):
    clinic_id: str
    doctor_id: Optional[str] = Field(None)
    booking_type: str = Field(..., pattern="^(at_clinic|home_visit)$")
    scheduled_at: datetime
    duration_minutes: int = Field(default=30, ge=30, le=120)
    home_address: Optional[str] = None
    home_lat: Optional[float] = Field(None, ge=-90, le=90)
    home_lng: Optional[float] = Field(None, ge=-180, le=180)
    notes: Optional[str] = None
    payment_method: str = Field(default="cash", pattern="^(cash|transfer)$")

    @field_validator("scheduled_at", mode="before")
    @classmethod
    def parse_scheduled_at(cls, v):
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            try:
                dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
                if dt.tzinfo is not None:
                    return dt.replace(tzinfo=None)
                return dt
            except Exception:
                pass
        return v


class BookingUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=30, le=120)
    notes: Optional[str] = None


class BookingStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(confirmed|in_progress|completed)$")


class AdminBookingStatusUpdate(BaseModel):
    """Admin or clinic owner can set any status"""
    status: str = Field(
        ...,
        pattern="^(pending|confirmed|in_progress|completed|cancelled|expired)$",
    )
    cancellation_reason: Optional[str] = None


class BookingCancel(BaseModel):
    reason: Optional[str] = None


class BookingResponse(BaseModel):
    id: str
    user_id: str
    clinic_id: str
    doctor_id: str
    booking_type: str
    scheduled_at: datetime
    duration_minutes: int
    status: str
    home_address: Optional[str] = None
    home_lat: Optional[float] = None
    home_lng: Optional[float] = None
    notes: Optional[str] = None
    total_price: Optional[float] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    cancellation_reason: Optional[str] = None
    cancelled_by: Optional[str] = None
    cancelled_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookingListResponse(BaseModel):
    bookings: list[BookingResponse]
    total: int
    page: int
    page_size: int


class SlotResponse(BaseModel):
    id: str
    doctor_id: str
    slot_start: datetime
    slot_end: datetime
    is_available: bool

    class Config:
        from_attributes = True
