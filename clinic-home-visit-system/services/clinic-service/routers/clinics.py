"""
Clinic Service - Clinics Router
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from pydantic import BaseModel
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from clinic_service.models.models import Clinic
from clinic_service.schemas.schemas import (
    ClinicCreate, ClinicUpdate, ClinicResponse, ClinicListResponse,
)
from clinic_service.utils.dependencies import (
    get_db, optional_user, require_user, require_admin, require_clinic_owner_or_admin,
)
from shared.gps.haversine import (
    calculate_haversine_distance,
    estimate_travel_time,
)


router = APIRouter()


@router.get("", response_model=ClinicListResponse)
async def list_clinics(
    lat: Optional[float] = Query(None, ge=-90, le=90),
    lng: Optional[float] = Query(None, ge=-180, le=180),
    radius_km: float = Query(default=10.0, ge=0.5, le=50),
    sort_by: str = Query(default="distance"),
    specialty: Optional[str] = Query(None),
    supports_home_visit: Optional[bool] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    is_verified: Optional[bool] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """List clinics with GPS-based filtering and sorting"""
    query = select(Clinic).where(Clinic.is_active == True)

    # Non-GPS filters
    if specialty:
        query = query.where(Clinic.specialties.contains([specialty.lower()]))
    if supports_home_visit is not None:
        query = query.where(Clinic.supports_home_visit == supports_home_visit)
    if is_verified is not None:
        query = query.where(Clinic.is_verified == is_verified)
    if min_price is not None:
        query = query.where(Clinic.min_price >= min_price)
    if max_price is not None:
        query = query.where(Clinic.max_price <= max_price)
    if search:
        search_term = f"%{search.lower()}%"
        query = query.where(
            or_(
                Clinic.name.ilike(search_term),
                Clinic.address.ilike(search_term),
            )
        )

    # Fetch all clinics matching non-radius filters (no SQL spatial filter — done in Python)
    result = await db.execute(query)
    all_clinics = result.scalars().all()

    # Calculate distance and filter by exact haversine radius
    clinic_responses = []
    for clinic in all_clinics:
        clinic_lat = float(clinic.lat)
        clinic_lng = float(clinic.lng)

        distance_km = None
        estimated_time = None

        if lat is not None and lng is not None:
            distance_km = calculate_haversine_distance(lat, lng, clinic_lat, clinic_lng)
            estimated_time = estimate_travel_time(distance_km, "driving")
            # Exclude clinics outside the exact radius
            if distance_km > radius_km:
                continue

        clinic_responses.append(ClinicResponse(
            id=str(clinic.id),
            name=clinic.name,
            address=clinic.address,
            lat=clinic_lat,
            lng=clinic_lng,
            phone=clinic.phone,
            email=clinic.email,
            specialties=clinic.specialties or [],
            opening_time=clinic.opening_time,
            closing_time=clinic.closing_time,
            supports_home_visit=clinic.supports_home_visit,
            home_visit_radius_km=float(clinic.home_visit_radius_km or 10),
            min_price=float(clinic.min_price) if clinic.min_price else None,
            max_price=float(clinic.max_price) if clinic.max_price else None,
            images=clinic.images or [],
            owner_id=str(clinic.owner_id) if clinic.owner_id else None,
            is_active=clinic.is_active,
            is_verified=clinic.is_verified,
            data_source=clinic.data_source,
            confidence_score=float(clinic.confidence_score or 1.0),
            distance_km=distance_km,
            estimated_travel_time_min=estimated_time,
            created_at=clinic.created_at,
            updated_at=clinic.updated_at,
        ))

    # Sort by distance if GPS provided
    if lat is not None and lng is not None and sort_by == "distance":
        clinic_responses.sort(key=lambda x: x.distance_km or float('inf'))

    total = len(clinic_responses)

    # Apply pagination on the filtered+sorted list
    offset = (page - 1) * page_size
    paginated = clinic_responses[offset:offset + page_size]

    return ClinicListResponse(
        clinics=paginated,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/nearby")
async def get_nearby_clinics(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(default=10.0, ge=0.5, le=50),
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Get nearby clinics sorted by distance"""
    result = await db.execute(
        select(Clinic).where(Clinic.is_active == True)
    )
    clinics = result.scalars().all()

    nearby = []
    for clinic in clinics:
        clinic_lat = float(clinic.lat)
        clinic_lng = float(clinic.lng)
        distance = calculate_haversine_distance(lat, lng, clinic_lat, clinic_lng)

        if distance <= radius_km:
            nearby.append({
                "id": str(clinic.id),
                "name": clinic.name,
                "address": clinic.address,
                "lat": clinic_lat,
                "lng": clinic_lng,
                "specialties": clinic.specialties or [],
                "distance_km": round(distance, 2),
                "estimated_travel_time_min": estimate_travel_time(distance, "driving"),
            })

    nearby.sort(key=lambda x: x["distance_km"])
    return {"clinics": nearby[:limit], "total": len(nearby)}


@router.get("/{clinic_id}")
async def get_clinic(
    clinic_id: str,
    lat: Optional[float] = Query(None, ge=-90, le=90),
    lng: Optional[float] = Query(None, ge=-180, le=180),
    db: AsyncSession = Depends(get_db),
):
    """Get clinic details"""
    result = await db.execute(select(Clinic).where(Clinic.id == clinic_id))
    clinic = result.scalar_one_or_none()

    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinic not found")

    clinic_lat = float(clinic.lat)
    clinic_lng = float(clinic.lng)
    distance_km = None
    estimated_time = None

    if lat is not None and lng is not None:
        distance_km = calculate_haversine_distance(lat, lng, clinic_lat, clinic_lng)
        estimated_time = estimate_travel_time(distance_km, "driving")

    return ClinicResponse(
        id=str(clinic.id),
        name=clinic.name,
        address=clinic.address,
        lat=clinic_lat,
        lng=clinic_lng,
        phone=clinic.phone,
        email=clinic.email,
        specialties=clinic.specialties or [],
        opening_time=clinic.opening_time,
        closing_time=clinic.closing_time,
        supports_home_visit=clinic.supports_home_visit,
        home_visit_radius_km=float(clinic.home_visit_radius_km or 10),
        min_price=float(clinic.min_price) if clinic.min_price else None,
        max_price=float(clinic.max_price) if clinic.max_price else None,
        images=clinic.images or [],
        owner_id=str(clinic.owner_id) if clinic.owner_id else None,
        is_active=clinic.is_active,
        is_verified=clinic.is_verified,
        data_source=clinic.data_source,
        confidence_score=float(clinic.confidence_score or 1.0),
        distance_km=distance_km,
        estimated_travel_time_min=estimated_time,
        created_at=clinic.created_at,
        updated_at=clinic.updated_at,
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_clinic(
    request: ClinicCreate,
    admin_user: dict = Depends(require_clinic_owner_or_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a new clinic. Admin can set any owner_id; clinic_owner is auto-assigned as owner."""
    user_id = admin_user["user_id"]
    role = admin_user["role"]

    owner_id = request.owner_id
    if role == "clinic_owner":
        # Clinic owner can only create clinic for themselves
        owner_id = user_id

    clinic = Clinic(
        name=request.name,
        address=request.address,
        lat=request.lat,
        lng=request.lng,
        phone=request.phone,
        email=request.email,
        specialties=request.specialties,
        opening_time=request.opening_time,
        closing_time=request.closing_time,
        supports_home_visit=request.supports_home_visit,
        home_visit_radius_km=request.home_visit_radius_km,
        min_price=request.min_price,
        max_price=request.max_price,
        images=request.images,
        owner_id=owner_id,
    )
    db.add(clinic)
    await db.commit()
    await db.refresh(clinic)

    return ClinicResponse(
        id=str(clinic.id),
        name=clinic.name,
        address=clinic.address,
        lat=float(clinic.lat),
        lng=float(clinic.lng),
        phone=clinic.phone,
        email=clinic.email,
        specialties=clinic.specialties or [],
        opening_time=clinic.opening_time,
        closing_time=clinic.closing_time,
        supports_home_visit=clinic.supports_home_visit,
        home_visit_radius_km=float(clinic.home_visit_radius_km or 10),
        min_price=float(clinic.min_price) if clinic.min_price else None,
        max_price=float(clinic.max_price) if clinic.max_price else None,
        images=clinic.images or [],
        owner_id=str(clinic.owner_id) if clinic.owner_id else None,
        is_active=clinic.is_active,
        is_verified=clinic.is_verified,
        data_source=clinic.data_source,
        confidence_score=float(clinic.confidence_score or 1.0),
        created_at=clinic.created_at,
        updated_at=clinic.updated_at,
    )


@router.put("/{clinic_id}")
async def update_clinic(
    clinic_id: str,
    request: ClinicUpdate,
    admin_user: dict = Depends(require_clinic_owner_or_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a clinic. Admin can update any clinic; clinic_owner can only update their own."""
    user_id = admin_user["user_id"]
    role = admin_user["role"]

    result = await db.execute(select(Clinic).where(Clinic.id == clinic_id))
    clinic = result.scalar_one_or_none()

    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinic not found")

    # Ownership check for non-admin
    if role != "admin":
        if str(clinic.owner_id) != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this clinic")

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(clinic, key, value)

    await db.commit()
    await db.refresh(clinic)

    return ClinicResponse(
        id=str(clinic.id),
        name=clinic.name,
        address=clinic.address,
        lat=float(clinic.lat),
        lng=float(clinic.lng),
        phone=clinic.phone,
        email=clinic.email,
        specialties=clinic.specialties or [],
        opening_time=clinic.opening_time,
        closing_time=clinic.closing_time,
        supports_home_visit=clinic.supports_home_visit,
        home_visit_radius_km=float(clinic.home_visit_radius_km or 10),
        min_price=float(clinic.min_price) if clinic.min_price else None,
        max_price=float(clinic.max_price) if clinic.max_price else None,
        images=clinic.images or [],
        owner_id=str(clinic.owner_id) if clinic.owner_id else None,
        is_active=clinic.is_active,
        is_verified=clinic.is_verified,
        data_source=clinic.data_source,
        confidence_score=float(clinic.confidence_score or 1.0),
        created_at=clinic.created_at,
        updated_at=clinic.updated_at,
    )


@router.delete("/{clinic_id}")
async def delete_clinic(
    clinic_id: str,
    admin_user: dict = Depends(require_clinic_owner_or_admin),
    db: AsyncSession = Depends(get_db),
):
    """Delete a clinic (soft delete). Admin can delete any; clinic_owner can only delete their own."""
    user_id = admin_user["user_id"]
    role = admin_user["role"]

    result = await db.execute(select(Clinic).where(Clinic.id == clinic_id))
    clinic = result.scalar_one_or_none()

    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinic not found")

    if role != "admin" and str(clinic.owner_id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this clinic")

    clinic.is_active = False
    await db.commit()

    return {"message": "Clinic deleted"}


# ============ Clinic Owner Endpoints ============

@router.get("/owner/my-clinics")
async def get_owner_clinics(
    search: Optional[str] = Query(None),
    is_verified: Optional[bool] = Query(None),
    supports_home_visit: Optional[bool] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    staff_user: dict = Depends(require_clinic_owner_or_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get all clinics owned by the current clinic_owner or all clinics for admin."""
    user_id = staff_user["user_id"]
    role = staff_user["role"]

    # For clinic_owner, only get their own clinics
    if role == "clinic_owner":
        query = select(Clinic).where(
            Clinic.owner_id == user_id,
            Clinic.is_active == True
        )
    else:
        # Admin sees all active clinics
        query = select(Clinic).where(Clinic.is_active == True)

    # Apply filters
    if is_verified is not None:
        query = query.where(Clinic.is_verified == is_verified)
    if supports_home_visit is not None:
        query = query.where(Clinic.supports_home_visit == supports_home_visit)
    if search:
        search_term = f"%{search.lower()}%"
        query = query.where(
            or_(
                Clinic.name.ilike(search_term),
                Clinic.address.ilike(search_term),
            )
        )

    # Get total count
    from sqlalchemy import func
    count_query = select(func.count(Clinic.id))
    if role == "clinic_owner":
        count_query = count_query.where(
            Clinic.owner_id == user_id,
            Clinic.is_active == True
        )
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    query = query.order_by(Clinic.created_at.desc())

    result = await db.execute(query)
    clinics = result.scalars().all()

    # Get doctor counts for each clinic
    from clinic_service.models.models import Doctor
    from sqlalchemy import select as sa_select

    doctor_count_query = select(
        Doctor.clinic_id,
        func.count(Doctor.id).label("count")
    ).where(Doctor.is_active == True).group_by(Doctor.clinic_id)

    doctor_count_result = await db.execute(doctor_count_query)
    doctor_counts = {str(row.clinic_id): row.count for row in doctor_count_result}

    clinic_responses = []
    for clinic in clinics:
        clinic_responses.append(ClinicResponse(
            id=str(clinic.id),
            name=clinic.name,
            address=clinic.address,
            lat=float(clinic.lat),
            lng=float(clinic.lng),
            phone=clinic.phone,
            email=clinic.email,
            specialties=clinic.specialties or [],
            opening_time=clinic.opening_time,
            closing_time=clinic.closing_time,
            supports_home_visit=clinic.supports_home_visit,
            home_visit_radius_km=float(clinic.home_visit_radius_km or 10),
            min_price=float(clinic.min_price) if clinic.min_price else None,
            max_price=float(clinic.max_price) if clinic.max_price else None,
            images=clinic.images or [],
            owner_id=str(clinic.owner_id) if clinic.owner_id else None,
            is_active=clinic.is_active,
            is_verified=clinic.is_verified,
            data_source=clinic.data_source,
            confidence_score=float(clinic.confidence_score or 1.0),
            created_at=clinic.created_at,
            updated_at=clinic.updated_at,
            doctor_count=doctor_counts.get(str(clinic.id), 0),
        ))

    return ClinicListResponse(
        clinics=clinic_responses,
        total=total,
        page=page,
        page_size=page_size,
    )
