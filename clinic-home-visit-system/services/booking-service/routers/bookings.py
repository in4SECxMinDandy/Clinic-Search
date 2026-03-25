"""
Booking Service - Bookings Router
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from booking_service.models.models import Booking, BookingSlot
from booking_service.schemas.schemas import (
    BookingCreate, BookingUpdate, BookingStatusUpdate, BookingCancel,
    BookingResponse, BookingListResponse,
)
from booking_service.utils.dependencies import get_db, get_current_user
from shared.message_broker import get_message_broker
import structlog

logger = structlog.get_logger()
router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(
    request: BookingCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new booking"""
    # Validate not in the past
    if request.scheduled_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Cannot book in the past")

    # Check for slot availability
    result = await db.execute(
        select(Booking).where(
            and_(
                Booking.doctor_id == request.doctor_id,
                Booking.scheduled_at == request.scheduled_at,
                Booking.status.in_(["pending", "confirmed"]),
            )
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Time slot is not available")

    # Home visit validation
    if request.booking_type == "home_visit":
        if not request.home_address:
            raise HTTPException(status_code=400, detail="Home address required for home visit")
        if not request.home_lat or not request.home_lng:
            raise HTTPException(status_code=400, detail="Home coordinates required for home visit")

    booking = Booking(
        user_id=current_user["user_id"],
        clinic_id=request.clinic_id,
        doctor_id=request.doctor_id,
        booking_type=request.booking_type,
        scheduled_at=request.scheduled_at,
        duration_minutes=request.duration_minutes,
        home_address=request.home_address,
        home_lat=str(request.home_lat) if request.home_lat else None,
        home_lng=str(request.home_lng) if request.home_lng else None,
        notes=request.notes,
        payment_method=request.payment_method,
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    # Publish event
    try:
        broker = get_message_broker()
        await broker.publish_booking_created(
            booking_id=str(booking.id),
            user_id=str(booking.user_id),
            clinic_id=str(booking.clinic_id),
            doctor_id=str(booking.doctor_id),
            booking_type=booking.booking_type,
            scheduled_at=booking.scheduled_at.isoformat(),
        )
    except Exception as e:
        logger.error("event_publish_failed", error=str(e))

    return BookingResponse(
        id=str(booking.id),
        user_id=str(booking.user_id),
        clinic_id=str(booking.clinic_id),
        doctor_id=str(booking.doctor_id),
        booking_type=booking.booking_type,
        scheduled_at=booking.scheduled_at,
        duration_minutes=booking.duration_minutes,
        status=booking.status,
        home_address=booking.home_address,
        home_lat=float(booking.home_lat) if booking.home_lat else None,
        home_lng=float(booking.home_lng) if booking.home_lng else None,
        notes=booking.notes,
        total_price=float(booking.total_price) if booking.total_price else None,
        payment_method=booking.payment_method,
        payment_status=booking.payment_status,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
    )


@router.get("", response_model=BookingListResponse)
async def list_bookings(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List bookings for current user"""
    query = select(Booking).where(Booking.user_id == current_user["user_id"])

    if status_filter:
        query = query.where(Booking.status == status_filter)

    query = query.order_by(Booking.scheduled_at.desc())
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    bookings = result.scalars().all()

    return BookingListResponse(
        bookings=[
            BookingResponse(
                id=str(b.id),
                user_id=str(b.user_id),
                clinic_id=str(b.clinic_id),
                doctor_id=str(b.doctor_id),
                booking_type=b.booking_type,
                scheduled_at=b.scheduled_at,
                duration_minutes=b.duration_minutes,
                status=b.status,
                home_address=b.home_address,
                home_lat=float(b.home_lat) if b.home_lat else None,
                home_lng=float(b.home_lng) if b.home_lng else None,
                notes=b.notes,
                total_price=float(b.total_price) if b.total_price else None,
                payment_method=b.payment_method,
                payment_status=b.payment_status,
                cancellation_reason=b.cancellation_reason,
                cancelled_by=b.cancelled_by,
                cancelled_at=b.cancelled_at,
                confirmed_at=b.confirmed_at,
                completed_at=b.completed_at,
                created_at=b.created_at,
                updated_at=b.updated_at,
            )
            for b in bookings
        ],
        total=len(bookings),
        page=page,
        page_size=page_size,
    )


@router.get("/{booking_id}")
async def get_booking(
    booking_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get booking details"""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return BookingResponse(
        id=str(booking.id),
        user_id=str(booking.user_id),
        clinic_id=str(booking.clinic_id),
        doctor_id=str(booking.doctor_id),
        booking_type=booking.booking_type,
        scheduled_at=booking.scheduled_at,
        duration_minutes=booking.duration_minutes,
        status=booking.status,
        home_address=booking.home_address,
        home_lat=float(booking.home_lat) if booking.home_lat else None,
        home_lng=float(booking.home_lng) if booking.home_lng else None,
        notes=booking.notes,
        total_price=float(booking.total_price) if booking.total_price else None,
        payment_method=booking.payment_method,
        payment_status=booking.payment_status,
        cancellation_reason=booking.cancellation_reason,
        cancelled_by=booking.cancelled_by,
        cancelled_at=booking.cancelled_at,
        confirmed_at=booking.confirmed_at,
        completed_at=booking.completed_at,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
    )


@router.put("/{booking_id}/status")
async def update_booking_status(
    booking_id: str,
    request: BookingStatusUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update booking status"""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    update_data = {"status": request.status}
    if request.status == "confirmed":
        update_data["confirmed_at"] = datetime.utcnow()
    elif request.status == "completed":
        update_data["completed_at"] = datetime.utcnow()

    for key, value in update_data.items():
        setattr(booking, key, value)

    await db.commit()
    await db.refresh(booking)

    # Publish event
    try:
        broker = get_message_broker()
        await broker.publish(
            f"event:booking:{request.status}",
            {
                "booking_id": str(booking.id),
                "user_id": str(booking.user_id),
                "clinic_id": str(booking.clinic_id),
            },
        )
    except Exception as e:
        logger.error("event_publish_failed", error=str(e))

    return BookingResponse(
        id=str(booking.id),
        user_id=str(booking.user_id),
        clinic_id=str(booking.clinic_id),
        doctor_id=str(booking.doctor_id),
        booking_type=booking.booking_type,
        scheduled_at=booking.scheduled_at,
        duration_minutes=booking.duration_minutes,
        status=booking.status,
        home_address=booking.home_address,
        home_lat=float(booking.home_lat) if booking.home_lat else None,
        home_lng=float(booking.home_lng) if booking.home_lng else None,
        notes=booking.notes,
        total_price=float(booking.total_price) if booking.total_price else None,
        payment_method=booking.payment_method,
        payment_status=booking.payment_status,
        cancellation_reason=booking.cancellation_reason,
        cancelled_by=booking.cancelled_by,
        cancelled_at=booking.cancelled_at,
        confirmed_at=booking.confirmed_at,
        completed_at=booking.completed_at,
        created_at=booking.created_at,
        updated_at=booking.updated_at,
    )


@router.post("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: str,
    request: BookingCancel,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel a booking"""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status not in ["pending", "confirmed"]:
        raise HTTPException(status_code=400, detail="Cannot cancel this booking")

    # Check 2 hour rule
    time_until = booking.scheduled_at - datetime.utcnow()
    if time_until.total_seconds() < 2 * 3600:
        raise HTTPException(status_code=400, detail="Cannot cancel within 2 hours of appointment")

    booking.status = "cancelled"
    booking.cancellation_reason = request.reason
    booking.cancelled_by = "user"
    booking.cancelled_at = datetime.utcnow()

    await db.commit()
    await db.refresh(booking)

    # Publish event
    try:
        broker = get_message_broker()
        await broker.publish_booking_cancelled(
            booking_id=str(booking.id),
            user_id=str(booking.user_id),
            reason=request.reason or "User cancelled",
        )
    except Exception as e:
        logger.error("event_publish_failed", error=str(e))

    return {"message": "Booking cancelled", "booking_id": str(booking.id)}
