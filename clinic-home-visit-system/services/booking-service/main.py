"""
Booking Service - Main Application
"""
import sys
from pathlib import Path

# Add /app to path for shared module (works in Docker)
sys.path.insert(0, str(Path(__file__).parent))

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from booking_service.routers import bookings
from booking_service.utils.dependencies import set_database
from shared.config import get_settings
from shared.database import Database, get_database_url
from shared.redis_client import RedisClient, init_redis

settings = get_settings()
SCHEMA_NAME = "booking_schema"
SERVICE_PORT = 8002

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger()

db: Database = None
redis: RedisClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db, redis
    logger.info("booking_service_starting", version=settings.APP_VERSION)

    db_url = get_database_url(host="postgres", port=5432, database="postgres", schema=SCHEMA_NAME)
    db = Database(db_url, schema_name=SCHEMA_NAME)
    db.init()
    set_database(db)
    logger.info("database_connected")

    redis = await init_redis(settings.REDIS_URL)
    logger.info("redis_connected")

    yield

    await db.close()
    await redis.disconnect()
    logger.info("booking_service_shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Booking Management Service",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "booking-service", "version": settings.APP_VERSION}


@app.get("/health/ready")
async def health_ready():
    checks = {"database": False, "redis": False}
    try:
        async with db.async_session_factory() as session:
            from sqlalchemy import text
            await session.execute(text("SELECT 1"))
            checks["database"] = True
    except Exception as e:
        logger.error("db_health_check_failed", error=str(e))
    try:
        await redis.client.ping()
        checks["redis"] = True
    except Exception as e:
        logger.error("redis_health_check_failed", error=str(e))
    return {"status": "healthy" if all(checks.values()) else "unhealthy", "checks": checks}


@app.get("/health/live")
async def health_live():
    return {"status": "alive"}


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", "unknown")
    log = logger.bind(request_id=request_id, path=request.url.path)
    log.info("request_started", method=request.method)
    response = await call_next(request)
    log.info("request_completed", method=request.method, status=response.status_code)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=SERVICE_PORT, reload=settings.DEBUG)
