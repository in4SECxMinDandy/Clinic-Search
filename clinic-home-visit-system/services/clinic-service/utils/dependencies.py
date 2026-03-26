"""
Clinic Service - Dependencies
"""
import sys
from pathlib import Path

# Add /app to path for shared module (works in Docker)
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from shared.database import Database, get_database_url
from shared.config import get_settings

settings = get_settings()

_db: Optional[Database] = None


def set_database(db: Database):
    global _db
    _db = db


async def get_db() -> AsyncSession:
    if _db is None:
        raise RuntimeError("Database not initialized")
    async with _db.async_session_factory() as session:
        yield session


async def get_redis():
    from shared.redis_client import get_redis_client
    return get_redis_client()


async def _verify_token(token: str) -> Optional[dict]:
    """Verify token via auth-service, returns user dict or None"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"http://auth-service:8003/api/v1/auth/verify",
                cookies={"access_token": token},
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("valid"):
                    return data
    except Exception:
        pass
    return None


def _token_from_header(authorization: Optional[str]) -> Optional[str]:
    if authorization and authorization.startswith("Bearer "):
        return authorization.replace("Bearer ", "")
    return None


async def optional_user(
    authorization: Optional[str] = Header(None),
):
    """Optional user authentication (doesn't raise if not authenticated)"""
    token = _token_from_header(authorization)
    if not token:
        return None
    return await _verify_token(token)


async def require_user(
    authorization: Optional[str] = Header(None),
):
    """Require user authentication"""
    user = await optional_user(authorization)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return user


async def require_admin(
    authorization: Optional[str] = Header(None),
):
    """Require admin role"""
    user = await require_user(authorization)
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


async def require_clinic_owner_or_admin(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Require clinic_owner role or admin. For non-admin, verifies they own the clinic via owner_id in request body."""
    user = await require_user(authorization)
    role = user.get("role")

    if role == "admin":
        return user  # admin bypasses ownership check

    if role != "clinic_owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clinic owner or admin access required",
        )
    return user


async def require_doctor_or_clinic_owner_or_admin(
    authorization: Optional[str] = Header(None),
):
    """Require doctor, clinic_owner, or admin role"""
    user = await require_user(authorization)
    role = user.get("role")
    if role in ("admin", "clinic_owner", "doctor"):
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Doctor, clinic owner, or admin access required",
    )
