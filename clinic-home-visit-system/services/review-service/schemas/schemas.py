"""
Review Service - Pydantic Schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    booking_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None


class ReviewReply(BaseModel):
    reply: str


class ReviewReport(BaseModel):
    reason: str = Field(..., pattern="^(spam|harassment|inappropriate|false_information|other)$")
    description: Optional[str] = None


class ReviewResponse(BaseModel):
    id: str
    booking_id: str
    user_id: str
    clinic_id: str
    doctor_id: str
    rating: int
    comment: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    is_hidden: bool
    hidden_reason: Optional[str] = None
    reply: Optional[str] = None
    replied_by: Optional[str] = None
    replied_at: Optional[datetime] = None
    is_reported: bool
    report_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
