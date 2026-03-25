"""
Auth Service - User Location Router
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.models.models import User, UserLocation
from auth_service.schemas.schemas import LocationCreate, LocationUpdate, LocationResponse
from auth_service.utils.dependencies import get_current_user, get_db

router = APIRouter()


@router.get("", response_model=list[LocationResponse])
async def get_user_locations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all locations for current user"""
    result = await db.execute(
        select(UserLocation)
        .where(UserLocation.user_id == current_user.id)
        .order_by(UserLocation.is_default.desc(), UserLocation.created_at.desc())
    )
    locations = result.scalars().all()

    return [
        LocationResponse(
            id=str(loc.id),
            user_id=str(loc.user_id),
            label=loc.label,
            address=loc.address,
            lat=float(loc.lat),
            lng=float(loc.lng),
            is_default=loc.is_default,
            created_at=loc.created_at,
            updated_at=loc.updated_at,
        )
        for loc in locations
    ]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_location(
    request: LocationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new location"""
    # If this is default, unset other defaults
    if request.is_default:
        await db.execute(
            update(UserLocation)
            .where(UserLocation.user_id == current_user.id)
            .values(is_default=False)
        )

    location = UserLocation(
        user_id=current_user.id,
        label=request.label,
        address=request.address,
        lat=str(request.lat),
        lng=str(request.lng),
        is_default=request.is_default,
    )
    db.add(location)
    await db.commit()
    await db.refresh(location)

    return LocationResponse(
        id=str(location.id),
        user_id=str(location.user_id),
        label=location.label,
        address=location.address,
        lat=float(location.lat),
        lng=float(location.lng),
        is_default=location.is_default,
        created_at=location.created_at,
        updated_at=location.updated_at,
    )


@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: str,
    request: LocationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a location"""
    result = await db.execute(
        select(UserLocation)
        .where(UserLocation.id == location_id)
        .where(UserLocation.user_id == current_user.id)
    )
    location = result.scalar_one_or_none()

    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    # If setting as default, unset others
    if request.is_default:
        await db.execute(
            update(UserLocation)
            .where(UserLocation.user_id == current_user.id)
            .where(UserLocation.id != location_id)
            .values(is_default=False)
        )

    update_data = request.model_dump(exclude_unset=True)
    if update_data:
        for key, value in update_data.items():
            if key in ["lat", "lng"] and value is not None:
                setattr(location, key, str(value))
            else:
                setattr(location, key, value)

    await db.commit()
    await db.refresh(location)

    return LocationResponse(
        id=str(location.id),
        user_id=str(location.user_id),
        label=location.label,
        address=location.address,
        lat=float(location.lat),
        lng=float(location.lng),
        is_default=location.is_default,
        created_at=location.created_at,
        updated_at=location.updated_at,
    )


@router.delete("/{location_id}")
async def delete_location(
    location_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a location"""
    result = await db.execute(
        select(UserLocation)
        .where(UserLocation.id == location_id)
        .where(UserLocation.user_id == current_user.id)
    )
    location = result.scalar_one_or_none()

    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    await db.delete(location)
    await db.commit()

    return {"message": "Location deleted"}


@router.post("/{location_id}/set-default")
async def set_default_location(
    location_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set a location as default"""
    result = await db.execute(
        select(UserLocation)
        .where(UserLocation.id == location_id)
        .where(UserLocation.user_id == current_user.id)
    )
    location = result.scalar_one_or_none()

    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    # Unset all defaults
    await db.execute(
        update(UserLocation)
        .where(UserLocation.user_id == current_user.id)
        .values(is_default=False)
    )

    # Set this one as default
    await db.execute(
        update(UserLocation)
        .where(UserLocation.id == location_id)
        .values(is_default=True)
    )
    await db.commit()

    return {"message": "Location set as default"}
