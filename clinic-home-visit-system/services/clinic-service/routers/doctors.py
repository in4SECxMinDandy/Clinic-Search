"""
Clinic Service - Doctors Router
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import time, datetime, timedelta

from clinic_service.models.models import Doctor, DoctorSchedule, Clinic
from clinic_service.schemas.schemas import (
    DoctorCreate, DoctorUpdate, DoctorResponse, ScheduleCreate, ScheduleResponse,
)
from clinic_service.utils.dependencies import get_db

router = APIRouter()


@router.get("", response_model=list[DoctorResponse])
async def list_doctors(
    clinic_id: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    supports_home_visit: Optional[bool] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all doctors with filters"""
    query = select(Doctor).where(Doctor.is_active == True)

    if clinic_id:
        query = query.where(Doctor.clinic_id == clinic_id)
    if specialty:
        query = query.where(Doctor.specialty.ilike(f"%{specialty}%"))
    if supports_home_visit is not None:
        query = query.where(Doctor.supports_home_visit == supports_home_visit)

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    doctors = result.scalars().all()

    return [
        DoctorResponse(
            id=str(doc.id),
            clinic_id=str(doc.clinic_id),
            name=doc.name,
            specialty=doc.specialty,
            license_number=doc.license_number,
            experience_years=doc.experience_years,
            avatar=doc.avatar,
            bio=doc.bio,
            supports_home_visit=doc.supports_home_visit,
            available_home_visit_radius_km=float(doc.available_home_visit_radius_km or 5),
            is_verified=doc.is_verified,
            is_active=doc.is_active,
            rating=float(doc.rating or 0),
            total_reviews=doc.total_reviews or 0,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
        )
        for doc in doctors
    ]


@router.get("/{doctor_id}")
async def get_doctor(doctor_id: str, db: AsyncSession = Depends(get_db)):
    """Get doctor details"""
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    return DoctorResponse(
        id=str(doctor.id),
        clinic_id=str(doctor.clinic_id),
        name=doctor.name,
        specialty=doctor.specialty,
        license_number=doctor.license_number,
        experience_years=doctor.experience_years,
        avatar=doctor.avatar,
        bio=doctor.bio,
        supports_home_visit=doctor.supports_home_visit,
        available_home_visit_radius_km=float(doctor.available_home_visit_radius_km or 5),
        is_verified=doctor.is_verified,
        is_active=doctor.is_active,
        rating=float(doctor.rating or 0),
        total_reviews=doctor.total_reviews or 0,
        created_at=doctor.created_at,
        updated_at=doctor.updated_at,
    )


@router.get("/{doctor_id}/schedules")
async def get_doctor_schedules(doctor_id: str, db: AsyncSession = Depends(get_db)):
    """Get doctor schedule"""
    result = await db.execute(
        select(DoctorSchedule)
        .where(DoctorSchedule.doctor_id == doctor_id)
        .where(DoctorSchedule.is_active == True)
        .order_by(DoctorSchedule.day_of_week)
    )
    schedules = result.scalars().all()

    return [
        ScheduleResponse(
            id=str(s.id),
            doctor_id=str(s.doctor_id),
            day_of_week=s.day_of_week,
            start_time=s.start_time,
            end_time=s.end_time,
            slot_duration_minutes=s.slot_duration_minutes,
            is_active=s.is_active,
        )
        for s in schedules
    ]


@router.get("/{doctor_id}/slots")
async def get_available_slots(
    doctor_id: str,
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    duration_minutes: int = Query(default=30, ge=15, le=120),
    db: AsyncSession = Depends(get_db),
):
    """Get available booking slots for a doctor on a date"""
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    day_of_week = target_date.weekday()  # 0=Monday, 6=Sunday

    # Get doctor schedule for this day
    result = await db.execute(
        select(DoctorSchedule)
        .where(DoctorSchedule.doctor_id == doctor_id)
        .where(DoctorSchedule.day_of_week == day_of_week)
        .where(DoctorSchedule.is_active == True)
    )
    schedule = result.scalar_one_or_none()

    if not schedule:
        return {"slots": [], "message": "No schedule for this day"}

    # Generate time slots
    slots = []
    current_time = datetime.combine(target_date, schedule.start_time)
    end_time = datetime.combine(target_date, schedule.end_time)

    while current_time + timedelta(minutes=duration_minutes) <= end_time:
        slots.append({
            "start": current_time.isoformat(),
            "end": (current_time + timedelta(minutes=duration_minutes)).isoformat(),
            "available": True,  # TODO: Check against existing bookings
        })
        current_time += timedelta(minutes=schedule.slot_duration_minutes)

    return {"doctor_id": doctor_id, "date": date, "slots": slots}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_doctor(request: DoctorCreate, db: AsyncSession = Depends(get_db)):
    """Create a new doctor"""
    # Verify clinic exists
    clinic_result = await db.execute(select(Clinic).where(Clinic.id == request.clinic_id))
    if not clinic_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Clinic not found")

    doctor = Doctor(
        clinic_id=request.clinic_id,
        name=request.name,
        specialty=request.specialty,
        license_number=request.license_number,
        experience_years=request.experience_years,
        avatar=request.avatar,
        bio=request.bio,
        supports_home_visit=request.supports_home_visit,
        available_home_visit_radius_km=request.available_home_visit_radius_km,
    )
    db.add(doctor)
    await db.commit()
    await db.refresh(doctor)

    return DoctorResponse(
        id=str(doctor.id),
        clinic_id=str(doctor.clinic_id),
        name=doctor.name,
        specialty=doctor.specialty,
        license_number=doctor.license_number,
        experience_years=doctor.experience_years,
        avatar=doctor.avatar,
        bio=doctor.bio,
        supports_home_visit=doctor.supports_home_visit,
        available_home_visit_radius_km=float(doctor.available_home_visit_radius_km or 5),
        is_verified=doctor.is_verified,
        is_active=doctor.is_active,
        rating=float(doctor.rating or 0),
        total_reviews=doctor.total_reviews or 0,
        created_at=doctor.created_at,
        updated_at=doctor.updated_at,
    )


@router.post("/{doctor_id}/schedules", status_code=status.HTTP_201_CREATED)
async def create_schedule(
    doctor_id: str,
    request: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create schedule for doctor"""
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Doctor not found")

    schedule = DoctorSchedule(
        doctor_id=doctor_id,
        day_of_week=request.day_of_week,
        start_time=request.start_time,
        end_time=request.end_time,
        slot_duration_minutes=request.slot_duration_minutes,
    )
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)

    return ScheduleResponse(
        id=str(schedule.id),
        doctor_id=str(schedule.doctor_id),
        day_of_week=schedule.day_of_week,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        slot_duration_minutes=schedule.slot_duration_minutes,
        is_active=schedule.is_active,
    )


@router.put("/{doctor_id}")
async def update_doctor(
    doctor_id: str,
    request: DoctorUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update doctor"""
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(doctor, key, value)

    await db.commit()
    await db.refresh(doctor)

    return DoctorResponse(
        id=str(doctor.id),
        clinic_id=str(doctor.clinic_id),
        name=doctor.name,
        specialty=doctor.specialty,
        license_number=doctor.license_number,
        experience_years=doctor.experience_years,
        avatar=doctor.avatar,
        bio=doctor.bio,
        supports_home_visit=doctor.supports_home_visit,
        available_home_visit_radius_km=float(doctor.available_home_visit_radius_km or 5),
        is_verified=doctor.is_verified,
        is_active=doctor.is_active,
        rating=float(doctor.rating or 0),
        total_reviews=doctor.total_reviews or 0,
        created_at=doctor.created_at,
        updated_at=doctor.updated_at,
    )


@router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: str, db: AsyncSession = Depends(get_db)):
    """Delete doctor (soft delete)"""
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    doctor.is_active = False
    await db.commit()

    return {"message": "Doctor deleted"}
