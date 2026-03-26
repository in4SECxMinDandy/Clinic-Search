"""
Clinic Service - Pydantic Schemas
"""
from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class ClinicBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1)
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    specialties: list[str] = Field(..., min_length=1)
    opening_time: time
    closing_time: time
    supports_home_visit: bool = False
    home_visit_radius_km: float = Field(default=10.0, ge=0, le=50)
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    images: Optional[list[str]] = None

    @field_validator("specialties")
    @classmethod
    def validate_specialties(cls, v):
        if not v:
            raise ValueError("At least one specialty is required")
        return [s.strip().lower() for s in v]


class ClinicCreate(ClinicBase):
    owner_id: Optional[str] = None


class ClinicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1)
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lng: Optional[float] = Field(None, ge=-180, le=180)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    specialties: Optional[list[str]] = Field(None, min_length=1)
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    supports_home_visit: Optional[bool] = None
    home_visit_radius_km: Optional[float] = Field(None, ge=0, le=50)
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    images: Optional[list[str]] = None
    is_active: Optional[bool] = None


class ClinicResponse(ClinicBase):
    id: str
    owner_id: Optional[str] = None
    is_active: bool
    is_verified: bool
    data_source: str
    confidence_score: float
    distance_km: Optional[float] = None
    estimated_travel_time_min: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    doctor_count: Optional[int] = None

    class Config:
        from_attributes = True


class ClinicListResponse(BaseModel):
    clinics: list[ClinicResponse]
    total: int
    page: int
    page_size: int


class DoctorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    specialty: str = Field(..., min_length=1, max_length=100)
    license_number: Optional[str] = Field(None, max_length=50)
    experience_years: int = Field(default=0, ge=0)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    supports_home_visit: bool = False
    available_home_visit_radius_km: float = Field(default=5.0, ge=0, le=50)


class DoctorCreate(DoctorBase):
    clinic_id: str


class DoctorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    specialty: Optional[str] = Field(None, min_length=1, max_length=100)
    license_number: Optional[str] = Field(None, max_length=50)
    experience_years: Optional[int] = Field(None, ge=0)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    supports_home_visit: Optional[bool] = None
    available_home_visit_radius_km: Optional[float] = Field(None, ge=0, le=50)
    is_active: Optional[bool] = None


class DoctorResponse(DoctorBase):
    id: str
    clinic_id: str
    is_verified: bool
    is_active: bool
    rating: float
    total_reviews: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScheduleBase(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: time
    end_time: time
    slot_duration_minutes: int = Field(default=30, ge=15, le=60)


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleResponse(ScheduleBase):
    id: str
    doctor_id: str
    is_active: bool

    class Config:
        from_attributes = True


class ClinicSearchParams(BaseModel):
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lng: Optional[float] = Field(None, ge=-180, le=180)
    radius_km: float = Field(default=10.0, ge=0.5, le=50)
    sort_by: str = Field(default="distance")
    specialty: Optional[str] = None
    supports_home_visit: Optional[bool] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    is_verified: Optional[bool] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    search: Optional[str] = None
