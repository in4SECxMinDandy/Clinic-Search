"""
Review Service - Main Application
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

from review_service.routers import reviews
from review_service.utils.dependencies import set_database
from shared.config import get_settings
from shared.database import Database, get_database_url

settings = get_settings()
SCHEMA_NAME = "review_schema"
SERVICE_PORT = 8004

structlog.configure(processors=[structlog.processors.add_log_level, structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()])
logger = structlog.get_logger()

db: Database = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db
    logger.info("review_service_starting")
    db_url = get_database_url(host="postgres", port=5432, database="postgres", schema="review_schema")
    db = Database(db_url, schema_name="review_schema")
    db.init()
    set_database(db)
    yield
    await db.close()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, description="Review Management Service", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])

@app.get("/health")
async def health(): return {"status": "healthy", "service": "review-service", "version": settings.APP_VERSION}

@app.get("/health/ready")
async def health_ready():
    try:
        async with db.async_session_factory() as session:
            from sqlalchemy import text
            await session.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except:
        return {"status": "unhealthy"}

@app.get("/health/live")
async def health_live(): return {"status": "alive"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=settings.DEBUG)
