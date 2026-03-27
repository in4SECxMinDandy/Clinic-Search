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
    BookingResponse, BookingListResponse, AdminBookingStatusUpdate,
)
from booking_service.utils.dependencies import (
    get_db, get_current_user, get_current_admin_user,
    get_clinic_owner_or_admin_user, get_doctor_or_admin_user,
)
from shared.message_broker import get_message_broker
import structlog

logger = structlog.get_logger()
router = APIRouter()


def _booking_to_response(b):
    return BookingResponse(
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


def _build_booking_response(booking: Booking) -> BookingResponse:
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


# ============ User Endpoints ============

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_booking(
    request: BookingCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new booking"""
    if request.scheduled_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Cannot book in the past")

    if request.doctor_id:
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
        home_lat=request.home_lat,
        home_lng=request.home_lng,
        notes=request.notes,
        payment_method=request.payment_method,
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)

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

    return _build_booking_response(booking)


@router.get("", response_model=BookingListResponse)
async def list_my_bookings(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List bookings for current user (only their own)"""
    from sqlalchemy import func
    query = select(Booking).where(Booking.user_id == current_user["user_id"])
    count_query = select(func.count(Booking.id)).where(Booking.user_id == current_user["user_id"])

    if status_filter:
        query = query.where(Booking.status == status_filter)
        count_query = count_query.where(Booking.status == status_filter)

    query = query.order_by(Booking.scheduled_at.desc())
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    total_result = await db.execute(count_query)
    bookings = result.scalars().all()
    total = total_result.scalar() or 0

    return BookingListResponse(
        bookings=[_build_booking_response(b) for b in bookings],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{booking_id}")
async def get_booking(
    booking_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get booking details (owner or admin/clinic_owner/doctor)"""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    role = current_user.get("role")
    if role != "admin" and str(booking.user_id) != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this booking")

    return _build_booking_response(booking)


@router.put("/{booking_id}/status")
async def user_update_booking_status(
    booking_id: str,
    request: BookingStatusUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """User endpoint: update status of their own booking (in_progress/completed only)"""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Ownership check
    if str(booking.user_id) != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this booking")

    # Only allow in_progress and completed
    if request.status not in ("in_progress", "completed"):
        raise HTTPException(status_code=400, detail="Patients can only set status to in_progress or completed")

    booking.status = request.status
    if request.status == "completed":
        booking.completed_at = datetime.utcnow()

    await db.commit()
    await db.refresh(booking)

    return _build_booking_response(booking)


@router.post("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: str,
    request: BookingCancel,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel a booking (only owner or admin can cancel)"""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    role = current_user.get("role")
    is_owner = str(booking.user_id) == current_user["user_id"]

    # Only owner or admin can cancel
    if role != "admin" and not is_owner:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this booking")

    if booking.status not in ["pending", "confirmed"]:
        raise HTTPException(status_code=400, detail="Cannot cancel this booking")

    # 2-hour rule only applies to the owner (admins bypass)
    if role != "admin":
        time_until = booking.scheduled_at - datetime.utcnow()
        if time_until.total_seconds() < 2 * 3600:
            raise HTTPException(status_code=400, detail="Cannot cancel within 2 hours of appointment")

    booking.status = "cancelled"
    booking.cancellation_reason = request.reason
    booking.cancelled_by = "admin" if role == "admin" else "user"
    booking.cancelled_at = datetime.utcnow()

    await db.commit()
    await db.refresh(booking)

    try:
        broker = get_message_broker()
        await broker.publish_booking_cancelled(
            booking_id=str(booking.id),
            user_id=str(booking.user_id),
            reason=request.reason or ("Admin cancelled" if role == "admin" else "User cancelled"),
        )
    except Exception as e:
        logger.error("event_publish_failed", error=str(e))

    return {"message": "Booking cancelled", "booking_id": str(booking.id)}


# ============ Admin / Clinic Owner / Doctor Endpoints ============

@router.get("/clinic/owner/all", response_model=BookingListResponse)
async def list_owner_clinic_bookings(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    clinic_id_filter: Optional[str] = Query(None, alias="clinic_id"),
    staff_user: dict = Depends(get_clinic_owner_or_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all bookings for clinics owned by the current clinic_owner or all clinics for admin."""
    from sqlalchemy import func

    user_id = staff_user["user_id"]
    role = staff_user["role"]

    # First get all clinic IDs owned by this user (for clinic_owner)
    if role == "clinic_owner":
        try:
            from booking_service.models.models import Clinic
            clinic_result = await db.execute(
                select(Clinic.id).where(Clinic.owner_id == user_id)
            )
            owned_clinic_ids = [row[0] for row in clinic_result.fetchall()]
        except Exception as e:
            logger.error("failed_to_query_owned_clinics", error=str(e))
            owned_clinic_ids = []

        if not owned_clinic_ids:
            return BookingListResponse(bookings=[], total=0, page=page, page_size=page_size)

        query = select(Booking).where(Booking.clinic_id.in_(owned_clinic_ids))
        count_query = select(func.count(Booking.id)).where(Booking.clinic_id.in_(owned_clinic_ids))
    else:
        # Admin sees all
        query = select(Booking)
        count_query = select(func.count(Booking.id))

    # Apply additional filters
    if status_filter:
        query = query.where(Booking.status == status_filter)
        count_query = count_query.where(Booking.status == status_filter)

    if clinic_id_filter:
        query = query.where(Booking.clinic_id == clinic_id_filter)
        count_query = count_query.where(Booking.clinic_id == clinic_id_filter)

    query = query.order_by(Booking.scheduled_at.desc())
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    total_result = await db.execute(count_query)
    bookings = result.scalars().all()
    total = total_result.scalar() or 0

    return BookingListResponse(
        bookings=[_build_booking_response(b) for b in bookings],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.put("/clinic/{clinic_id}/owner/update-status/{booking_id}")
async def owner_update_booking_status(
    clinic_id: str,
    booking_id: str,
    request: AdminBookingStatusUpdate,
    staff_user: dict = Depends(get_clinic_owner_or_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Clinic owner endpoint: update booking status for their own clinic."""
    from booking_service.models.models import Clinic

    user_id = staff_user["user_id"]
    role = staff_user["role"]

    # Verify ownership for clinic_owner
    if role == "clinic_owner":
        clinic_result = await db.execute(select(Clinic).where(Clinic.id == clinic_id))
        clinic = clinic_result.scalar_one_or_none()
        if not clinic or str(clinic.owner_id) != user_id:
            raise HTTPException(status_code=403, detail="You do not own this clinic")

    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if str(booking.clinic_id) != clinic_id:
        raise HTTPException(status_code=400, detail="Booking does not belong to this clinic")

    old_status = booking.status
    booking.status = request.status

    if request.status == "confirmed":
        booking.confirmed_at = datetime.utcnow()
    elif request.status == "completed":
        booking.completed_at = datetime.utcnow()
    elif request.status == "cancelled":
        booking.cancelled_at = datetime.utcnow()
        booking.cancelled_by = "clinic_owner"
        booking.cancellation_reason = request.cancellation_reason

    await db.commit()
    await db.refresh(booking)

    logger.info(
        "clinic_owner_booking_status_updated",
        user_id=str(user_id),
        booking_id=str(booking.id),
        clinic_id=clinic_id,
        old_status=old_status,
        new_status=request.status,
    )

    try:
        broker = get_message_broker()
        await broker.publish(
            f"event:booking:{request.status}",
            {
                "booking_id": str(booking.id),
                "user_id": str(booking.user_id),
                "clinic_id": str(booking.clinic_id),
                "updated_by": "clinic_owner",
            },
        )
    except Exception as e:
        logger.error("event_publish_failed", error=str(e))

    return _build_booking_response(booking)


@router.get("/clinic/{clinic_id}/all", response_model=BookingListResponse)
async def list_clinic_bookings(
    clinic_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    staff_user: dict = Depends(get_clinic_owner_or_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all bookings for a specific clinic. Admin sees all; clinic_owner sees only their clinics."""
    from sqlalchemy import func

    query = select(Booking).where(Booking.clinic_id == clinic_id)
    count_query = select(func.count(Booking.id)).where(Booking.clinic_id == clinic_id)

    if status_filter:
        query = query.where(Booking.status == status_filter)
        count_query = count_query.where(Booking.status == status_filter)

    query = query.order_by(Booking.scheduled_at.desc())
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    total_result = await db.execute(count_query)
    bookings = result.scalars().all()
    total = total_result.scalar() or 0

    return BookingListResponse(
        bookings=[_build_booking_response(b) for b in bookings],
        total=total,
        page=page,
        page_size=page_size,
    )


# ============ Admin Only Endpoints ============


@router.get("/admin/all", response_model=BookingListResponse)
async def admin_list_all_bookings(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    clinic_id_filter: Optional[str] = Query(None, alias="clinic_id"),
    user_id_filter: Optional[str] = Query(None, alias="user_id"),
    booking_type_filter: Optional[str] = Query(None, alias="booking_type"),
    admin_user: dict = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Admin endpoint: list all bookings across all users"""
    from sqlalchemy import func

    count_query = select(func.count(Booking.id))
    if status_filter:
        count_query = count_query.where(Booking.status == status_filter)
    if clinic_id_filter:
        count_query = count_query.where(Booking.clinic_id == clinic_id_filter)
    if user_id_filter:
        count_query = count_query.where(Booking.user_id == user_id_filter)
    if booking_type_filter:
        count_query = count_query.where(Booking.booking_type == booking_type_filter)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = select(Booking)
    if status_filter:
        query = query.where(Booking.status == status_filter)
    if clinic_id_filter:
        query = query.where(Booking.clinic_id == clinic_id_filter)
    if user_id_filter:
        query = query.where(Booking.user_id == user_id_filter)
    if booking_type_filter:
        query = query.where(Booking.booking_type == booking_type_filter)

    query = query.order_by(Booking.scheduled_at.desc())
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    bookings = result.scalars().all()

    return BookingListResponse(
        bookings=[_build_booking_response(b) for b in bookings],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/doctor/{doctor_id}/all", response_model=BookingListResponse)
async def list_doctor_bookings(
    doctor_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    staff_user: dict = Depends(get_doctor_or_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all bookings for a specific doctor. Admin sees all; doctor sees only their bookings."""
    from sqlalchemy import func

    query = select(Booking).where(Booking.doctor_id == doctor_id)
    count_query = select(func.count(Booking.id)).where(Booking.doctor_id == doctor_id)

    if status_filter:
        query = query.where(Booking.status == status_filter)
        count_query = count_query.where(Booking.status == status_filter)

    query = query.order_by(Booking.scheduled_at.desc())
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    total_result = await db.execute(count_query)
    bookings = result.scalars().all()
    total = total_result.scalar() or 0

    return BookingListResponse(
        bookings=[_build_booking_response(b) for b in bookings],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.put("/admin/{booking_id}/status")
async def admin_update_booking_status(
    booking_id: str,
    request: AdminBookingStatusUpdate,
    admin_user: dict = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Admin endpoint: update any booking status (approve/reject)"""
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    old_status = booking.status
    booking.status = request.status

    if request.status == "confirmed":
        booking.confirmed_at = datetime.utcnow()
    elif request.status == "completed":
        booking.completed_at = datetime.utcnow()
    elif request.status == "cancelled":
        booking.cancelled_at = datetime.utcnow()
        booking.cancelled_by = "admin"
        booking.cancellation_reason = request.cancellation_reason

    await db.commit()
    await db.refresh(booking)

    logger.info(
        "admin_booking_status_updated",
        admin_id=str(admin_user["user_id"]),
        booking_id=str(booking.id),
        old_status=old_status,
        new_status=request.status,
    )

    try:
        broker = get_message_broker()
        await broker.publish(
            f"event:booking:{request.status}",
            {
                "booking_id": str(booking.id),
                "user_id": str(booking.user_id),
                "clinic_id": str(booking.clinic_id),
                "updated_by": "admin",
            },
        )
    except Exception as e:
        logger.error("event_publish_failed", error=str(e))

    return _build_booking_response(booking)


@router.get("/admin/stats")
async def admin_get_booking_stats(
    admin_user: dict = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Admin endpoint: get booking statistics"""
    from sqlalchemy import func

    stats = {}

    status_query = select(
        Booking.status,
        func.count(Booking.id).label("count"),
    ).group_by(Booking.status)
    status_result = await db.execute(status_query)
    status_counts = {row.status: row.count for row in status_result}

    stats["by_status"] = {
        "pending": status_counts.get("pending", 0),
        "confirmed": status_counts.get("confirmed", 0),
        "in_progress": status_counts.get("in_progress", 0),
        "completed": status_counts.get("completed", 0),
        "cancelled": status_counts.get("cancelled", 0),
        "expired": status_counts.get("expired", 0),
    }
    stats["total"] = sum(stats["by_status"].values())

    type_query = select(
        Booking.booking_type,
        func.count(Booking.id).label("count"),
    ).group_by(Booking.booking_type)
    type_result = await db.execute(type_query)
    type_counts = {row.booking_type: row.count for row in type_result}

    stats["by_booking_type"] = {
        "at_clinic": type_counts.get("at_clinic", 0),
        "home_visit": type_counts.get("home_visit", 0),
    }

    return stats
