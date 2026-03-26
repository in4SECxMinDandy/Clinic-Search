"""
Data Collector Service - Database utilities
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import Database, get_database_url
from shared.config import get_settings

settings = get_settings()

# Module-level singleton
_db: Database | None = None


def get_database() -> Database:
    """Get or create database singleton."""
    global _db
    if _db is None:
        db_url = get_database_url(
            host="postgres",
            port=5432,
            database="postgres",
            schema="clinic_schema",
        )
        _db = Database(db_url, schema_name="clinic_schema")
        _db.init(async_only=True)
    return _db


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session."""
    db = get_database()
    async for session in db.get_async_session():
        yield session
