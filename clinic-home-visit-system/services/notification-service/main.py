"""
Notification Service - Main Application
"""
import sys
from pathlib import Path

# Add /app to path for shared module (works in Docker)
sys.path.insert(0, str(Path(__file__).parent))

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from notification_service.routers import notifications
from shared.config import get_settings
from shared.redis_client import RedisClient, init_redis

settings = get_settings()
SERVICE_PORT = 8005

structlog.configure(processors=[structlog.processors.add_log_level, structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()])
logger = structlog.get_logger()

redis: RedisClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    logger.info("notification_service_starting")
    redis = await init_redis(settings.REDIS_URL)
    yield
    await redis.disconnect()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, description="Notification Service", lifespan=lifespan)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])

@app.get("/health")
async def health(): return {"status": "healthy", "service": "notification-service", "version": settings.APP_VERSION}

@app.get("/health/ready")
async def health_ready():
    try:
        await redis.client.ping()
        return {"status": "healthy"}
    except:
        return {"status": "unhealthy"}

@app.get("/health/live")
async def health_live(): return {"status": "alive"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=settings.DEBUG)
