"""
Auth Service - User Management Router
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.models.models import User
from auth_service.schemas.schemas import UserResponse, UserUpdate, UserStatusUpdate
from auth_service.utils.dependencies import get_current_user, get_current_admin_user, get_db

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """Get current user profile"""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        role=current_user.role,
        is_active=current_user.is_active,
        email_verified_at=current_user.email_verified_at,
        last_login_at=current_user.last_login_at,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    request: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile"""
    update_data = request.model_dump(exclude_unset=True)

    if update_data:
        await db.execute(
            update(User)
            .where(User.id == current_user.id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(current_user)

    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        role=current_user.role,
        is_active=current_user.is_active,
        email_verified_at=current_user.email_verified_at,
        last_login_at=current_user.last_login_at,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get user by ID (admin or self)"""
    if current_user.role not in ["admin", "clinic_owner"] and str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        role=user.role,
        is_active=user.is_active,
        email_verified_at=user.email_verified_at,
        last_login_at=user.last_login_at,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


# ============ Admin User Management Endpoints ============


@router.get("/admin/all")
async def admin_list_all_users(
    page: int = 1,
    page_size: int = 20,
    role_filter: str = None,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user),
):
    """Admin endpoint: list all users"""
    from sqlalchemy import func, select

    # Count total
    count_query = select(func.count(User.id))
    if role_filter:
        count_query = count_query.where(User.role == role_filter)
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Fetch page
    query = select(User)
    if role_filter:
        query = query.where(User.role == role_filter)
    query = query.order_by(User.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    users = result.scalars().all()

    return {
        "users": [
            {
                "id": str(u.id),
                "email": u.email,
                "full_name": u.full_name,
                "phone": u.phone,
                "role": u.role,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.put("/admin/{user_id}/role")
async def admin_update_user_role(
    user_id: str,
    new_role: str = Query(..., alias="new_role"),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user),
):
    """Admin endpoint: update user role"""
    valid_roles = ["patient", "doctor", "clinic_owner", "admin"]
    if new_role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {valid_roles}")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    old_role = user.role
    user.role = new_role
    await db.commit()

    return {
        "message": "User role updated",
        "user_id": str(user.id),
        "old_role": old_role,
        "new_role": new_role,
    }


@router.put("/admin/{user_id}/status")
async def admin_toggle_user_status(
    user_id: str,
    request: UserStatusUpdate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user),
):
    """Admin endpoint: activate/deactivate user"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = request.is_active
    await db.commit()

    return {
        "message": f"User {'activated' if request.is_active else 'deactivated'}",
        "user_id": str(user.id),
        "is_active": request.is_active,
    }
