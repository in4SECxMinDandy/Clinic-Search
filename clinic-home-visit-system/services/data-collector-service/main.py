"""
Data Collector Service - Main Application
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from data_collector_service.routers import collectors
from shared.config import get_settings

settings = get_settings()

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("data_collector_service_starting")
    yield
    logger.info("data_collector_service_shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Data Collection Service — HOT-OSM Vietnam Health Facilities Import",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
app.include_router(collectors.router, prefix="/api/v1/collectors", tags=["Collectors"])


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "data-collector-service", "version": settings.APP_VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8006, reload=settings.DEBUG)
