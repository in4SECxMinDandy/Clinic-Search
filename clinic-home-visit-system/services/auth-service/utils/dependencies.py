"""
Auth Service - Dependencies
"""
import sys
from pathlib import Path

# Add /app to path for shared module (works in Docker)
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status, Cookie, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.models.models import User
from auth_service.services.jwt_service import decode_token
from shared.database import Database, get_database_url
from shared.config import get_settings

settings = get_settings()

# Global database instance (set in main.py)
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


def _jwt_from_cookie_or_bearer(
    access_token: Optional[str],
    authorization: Optional[str],
) -> Optional[str]:
    if access_token:
        return access_token
    if authorization and authorization.startswith("Bearer "):
        return authorization.removeprefix("Bearer ").strip()
    return None


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    access_token: Optional[str] = Cookie(None),
    authorization: Optional[str] = Header(None),
) -> User:
    """JWT from HttpOnly access_token cookie or Authorization: Bearer (gateway / SPA)."""
    token = _jwt_from_cookie_or_bearer(access_token, authorization)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    sub = payload.get("sub")
    try:
        user_id = UUID(sub) if isinstance(sub, str) else sub
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency to ensure user is admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
