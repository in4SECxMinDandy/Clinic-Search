"""
Booking Service - Dependencies
"""
import sys
from pathlib import Path

# Add /app to path for shared module (works in Docker)
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from shared.config import get_settings
from shared.database import Database, get_database_url

settings = get_settings()

_db: Optional[Database] = None


def set_database(db: Database):
    """Set the global database instance"""
    global _db
    _db = db


async def get_db() -> AsyncSession:
    """Dependency to get database session"""
    if _db is None:
        raise RuntimeError("Database not initialized")
    async with _db.async_session_factory() as session:
        yield session


async def get_current_user(
    authorization: Optional[str] = Header(None),
):
    """Get current authenticated user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = authorization.replace("Bearer ", "")

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"http://auth-service:8003/api/v1/auth/verify",
                cookies={"access_token": token},
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("valid"):
                    return {
                        "user_id": data["user_id"],
                        "email": data["email"],
                        "role": data["role"],
                    }
    except Exception:
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


async def get_current_admin_user(
    current_user: dict = Depends(get_current_user),
):
    """Dependency to ensure user is admin"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


async def get_clinic_owner_or_admin_user(
    current_user: dict = Depends(get_current_user),
):
    """Dependency to ensure user is admin or clinic_owner"""
    if current_user.get("role") not in ("admin", "clinic_owner"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clinic owner or admin access required",
        )
    return current_user


async def get_doctor_or_admin_user(
    current_user: dict = Depends(get_current_user),
):
    """Dependency to ensure user is admin or doctor"""
    if current_user.get("role") not in ("admin", "doctor"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor or admin access required",
        )
    return current_user
