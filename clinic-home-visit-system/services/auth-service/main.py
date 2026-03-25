"""
Auth Service - Main Application
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

from auth_service.routers import auth, users, locations
from auth_service.utils.dependencies import set_database
from shared.config import get_settings
from shared.database import Database, get_database_url
from shared.redis_client import RedisClient, init_redis

settings = get_settings()
SCHEMA_NAME = "auth_schema"
SERVICE_PORT = 8003

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger()

# Database instance
db: Database = None
redis: RedisClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global db, redis

    # Startup
    logger.info("auth_service_starting", version=settings.APP_VERSION)

    # Initialize database
    db_url = get_database_url(
        host="postgres",
        port=5432,
        database="postgres",
        schema=SCHEMA_NAME,
    )
    db = Database(db_url, schema_name=SCHEMA_NAME)
    db.init()
    set_database(db)
    logger.info("database_connected")

    # Initialize Redis
    redis = await init_redis(settings.REDIS_URL)
    logger.info("redis_connected")

    yield

    # Shutdown
    await db.close()
    await redis.disconnect()
    logger.info("auth_service_shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Authentication and Authorization Service",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(locations.router, prefix="/api/v1/locations", tags=["Locations"])


@app.get("/health")
async def health():
    """Basic health check"""
    return {"status": "healthy", "service": "auth-service", "version": settings.APP_VERSION}


@app.get("/health/ready")
async def health_ready():
    """Readiness check - verifies DB and Redis connections"""
    checks = {"database": False, "redis": False}

    try:
        async with db.get_async_session() as session:
            await session.execute("SELECT 1")
            checks["database"] = True
    except Exception as e:
        logger.error("db_health_check_failed", error=str(e))

    try:
        await redis.client.ping()
        checks["redis"] = True
    except Exception as e:
        logger.error("redis_health_check_failed", error=str(e))

    all_healthy = all(checks.values())
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks,
    }


@app.get("/health/live")
async def health_live():
    """Liveness check"""
    return {"status": "alive"}


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Add request ID and logging to all requests"""
    request_id = request.headers.get("X-Request-ID", "unknown")
    log = logger.bind(request_id=request_id, path=request.url.path)

    log.info("request_started", method=request.method)
    response = await call_next(request)
    log.info(
        "request_completed",
        method=request.method,
        status=response.status_code,
    )
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=SERVICE_PORT,
        reload=settings.DEBUG,
    )
