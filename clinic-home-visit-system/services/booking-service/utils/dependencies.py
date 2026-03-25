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
    async with _db.get_async_session() as session:
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
