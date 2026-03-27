"""
Booking Service - SQLAlchemy Models
"""
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Clinic(Base):
    """Clinic model for querying owned clinics"""
    __tablename__ = "clinics"
    __table_args__ = {"schema": "clinic_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True)
    owner_id = Column(UUID(as_uuid=True))


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("duration_minutes >= 30 AND duration_minutes <= 120", name="valid_duration"),
        CheckConstraint("status IN ('pending', 'confirmed', 'in_progress', 'completed', 'cancelled', 'expired')", name="valid_status"),
        {"schema": "booking_schema"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    clinic_id = Column(UUID(as_uuid=True), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), nullable=True)
    booking_type = Column(String(20), nullable=False)  # 'at_clinic', 'home_visit'
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=30)
    status = Column(String(20), nullable=False, default="pending")
    home_address = Column(Text)
    home_lat = Column(Numeric(10, 8))
    home_lng = Column(Numeric(11, 8))
    notes = Column(Text)
    total_price = Column(Numeric(10, 2))
    payment_method = Column(String(20))  # 'cash', 'transfer', 'vnpay', 'momo'
    payment_status = Column(String(20), default="unpaid")
    payment_transaction_id = Column(String(100))
    cancellation_reason = Column(Text)
    cancelled_by = Column(String(20))
    cancelled_at = Column(DateTime(timezone=True))
    confirmed_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Booking {self.id} status={self.status}>"


class BookingSlot(Base):
    __tablename__ = "booking_slots"
    __table_args__ = {"schema": "booking_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), nullable=False)
    slot_start = Column(DateTime(timezone=True), nullable=False)
    slot_end = Column(DateTime(timezone=True), nullable=False)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("booking_schema.bookings.id"))
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<BookingSlot doctor={self.doctor_id} start={self.slot_start}>"
