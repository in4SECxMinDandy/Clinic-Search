"""
Database Connection and Session Management
"""
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import NullPool


class Base(DeclarativeBase):
    """SQLAlchemy declarative base"""

    pass


class Database:
    """Database connection manager for microservices"""

    def __init__(
        self,
        database_url: str,
        schema_name: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self.database_url = database_url
        self.schema_name = schema_name
        self.async_engine = None
        self.sync_engine = None
        self.async_session_factory = None
        self.sync_session_factory = None
        self.pool_size = pool_size
        self.max_overflow = max_overflow

    def create_async_engine(self) -> None:
        """Create async engine"""
        self.async_engine = create_async_engine(
            self.database_url,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true",
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_pre_ping=True,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    def create_sync_engine(self) -> None:
        """Create sync engine"""
        self.sync_engine = create_engine(
            self.database_url,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true",
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_pre_ping=True,
        )
        self.sync_session_factory = sessionmaker(
            bind=self.sync_engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    def init(self, async_only: bool = False) -> None:
        """Initialize database connections"""
        self.create_async_engine()
        if not async_only:
            self.create_sync_engine()

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get async database session"""
        if not self.async_session_factory:
            self.create_async_engine()

        async with self.async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    def get_sync_session(self) -> Session:
        """Get sync database session"""
        if not self.sync_session_factory:
            self.create_sync_engine()
        return self.sync_session_factory()

    async def close(self) -> None:
        """Close database connections"""
        if self.async_engine:
            await self.async_engine.dispose()
        if self.sync_engine:
            self.sync_engine.dispose()

    async def create_tables(self) -> None:
        """Create all tables"""
        if not self.async_engine:
            self.create_async_engine()
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        """Drop all tables"""
        if not self.async_engine:
            self.create_async_engine()
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


def get_database_url(
    host: str = "localhost",
    port: int = 5432,
    database: str = "postgres",
    username: str = "postgres",
    password: str = "postgres",
    schema: Optional[str] = None,
) -> str:
    """Build database URL"""
    url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
    if schema:
        url += f"?search_path={schema}"
    return url


def get_sync_database_url(
    host: str = "localhost",
    port: int = 5432,
    database: str = "postgres",
    username: str = "postgres",
    password: str = "postgres",
) -> str:
    """Build sync database URL"""
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"
