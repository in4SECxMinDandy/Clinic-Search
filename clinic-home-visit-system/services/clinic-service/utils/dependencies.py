"""
Clinic Service - Dependencies
"""
import sys
from pathlib import Path

# Add /app to path for shared module (works in Docker)
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Optional
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
    async with _db.get_async_session() as session:
        yield session


async def get_redis():
    from shared.redis_client import get_redis_client
    return get_redis_client()


async def optional_user(
    authorization: Optional[str] = Header(None),
):
    """Optional user authentication (doesn't raise if not authenticated)"""
    if not authorization or not authorization.startswith("Bearer "):
        return None

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
                    return data
    except Exception:
        pass

    return None


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
