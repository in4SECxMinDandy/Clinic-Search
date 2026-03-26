"""
Clinic Service - SQLAlchemy Models
"""
import uuid
from datetime import time
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Clinic(Base):
    __tablename__ = "clinics"
    __table_args__ = {"schema": "clinic_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    lat = Column(Numeric(10, 7), nullable=False)
    lng = Column(Numeric(10, 7), nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    specialties = Column(ARRAY(String), nullable=False)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    supports_home_visit = Column(Boolean, default=False)
    home_visit_radius_km = Column(Numeric(5, 2), default=10.0)
    min_price = Column(Numeric(10, 2))
    max_price = Column(Numeric(10, 2))
    images = Column(ARRAY(Text))
    owner_id = Column(UUID(as_uuid=True))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    data_source = Column(String(20), default="manual")
    confidence_score = Column(Numeric(3, 2), default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    doctors = relationship("Doctor", back_populates="clinic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Clinic {self.name}>"


class Doctor(Base):
    __tablename__ = "doctors"
    __table_args__ = {"schema": "clinic_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinic_schema.clinics.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    specialty = Column(String(100), nullable=False)
    license_number = Column(String(50))
    experience_years = Column(Integer, default=0)
    avatar = Column(Text)
    bio = Column(Text)
    supports_home_visit = Column(Boolean, default=False)
    available_home_visit_radius_km = Column(Numeric(5, 2), default=5.0)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    rating = Column(Numeric(3, 2), default=0.0)
    total_reviews = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    clinic = relationship("Clinic", back_populates="doctors")
    schedules = relationship("DoctorSchedule", back_populates="doctor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Doctor {self.name}>"


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"
    __table_args__ = {"schema": "clinic_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("clinic_schema.doctors.id", ondelete="CASCADE"))
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    slot_duration_minutes = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)

    doctor = relationship("Doctor", back_populates="schedules")

    def __repr__(self):
        return f"<DoctorSchedule doctor={self.doctor_id} day={self.day_of_week}>"
