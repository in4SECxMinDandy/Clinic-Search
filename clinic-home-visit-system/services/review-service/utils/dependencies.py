"""
Review Service - Dependencies
"""
import sys
from pathlib import Path

# Add /app to path for shared module (works in Docker)
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Optional
from fastapi import Depends, HTTPException, status, Header
import httpx
from shared.config import get_settings

settings = get_settings()

async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = authorization.replace("Bearer ", "")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"http://auth-service:8003/api/v1/auth/verify", cookies={"access_token": token})
            if response.status_code == 200:
                data = response.json()
                if data.get("valid"):
                    return {"user_id": data["user_id"], "email": data["email"], "role": data["role"]}
    except Exception:
        pass
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_db():
    from shared.database import Database, get_database_url
    db_url = get_database_url(host="postgres", port=5432, database="postgres", schema="review_schema")
    db = Database(db_url, schema_name="review_schema")
    db.init()
    async with db.get_async_session() as session:
        yield session
