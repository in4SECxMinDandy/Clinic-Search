"""
Data Collector Service - Main Application
"""
import sys
from pathlib import Path

# Add /app to path for shared module (works in Docker)
sys.path.insert(0, str(Path(__file__).parent))

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from data_collector_service.routers import collectors
from shared.config import get_settings
from shared.database import Database, get_database_url
from shared.redis_client import init_redis

settings = get_settings()
SCHEMA_NAME = "clinic_schema"
SERVICE_PORT = 8006

structlog.configure(processors=[structlog.processors.add_log_level, structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()])
logger = structlog.get_logger()

db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db
    logger.info("data_collector_service_starting")
    db_url = get_database_url(host="postgres", port=5432, database="postgres", schema="clinic_schema")
    db = Database(db_url, schema_name="clinic_schema")
    db.init()
    await init_redis(settings.REDIS_URL)
    yield
    await db.close()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, description="Data Collection Service", lifespan=lifespan)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
app.include_router(collectors.router, prefix="/api/v1/collectors", tags=["Collectors"])

@app.get("/health")
async def health(): return {"status": "healthy", "service": "data-collector-service", "version": settings.APP_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=settings.DEBUG)
