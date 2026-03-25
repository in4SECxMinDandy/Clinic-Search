"""
Review Service - SQLAlchemy Models
"""
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {"schema": "review_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    clinic_id = Column(UUID(as_uuid=True), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    pros = Column(Text)
    cons = Column(Text)
    is_hidden = Column(Boolean, default=False)
    hidden_reason = Column(String(255))
    reply = Column(Text)
    replied_by = Column(UUID(as_uuid=True))
    replied_at = Column(DateTime(timezone=True))
    is_reported = Column(Boolean, default=False)
    report_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ReviewReport(Base):
    __tablename__ = "review_reports"
    __table_args__ = {"schema": "review_schema"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id = Column(UUID(as_uuid=True), ForeignKey("review_schema.reviews.id", ondelete="CASCADE"), nullable=False)
    reporter_id = Column(UUID(as_uuid=True), nullable=False)
    reason = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="pending")
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
