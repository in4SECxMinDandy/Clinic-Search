"""
Data Collector Service - Collectors Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import structlog

logger = structlog.get_logger()
router = APIRouter()

class CrawlRequest(BaseModel):
    source: Optional[str] = None
    force: bool = False

@router.post("/crawl")
async def start_crawl(request: CrawlRequest):
    """Start a crawl job"""
    logger.info("crawl_started", source=request.source)
    return {"message": "Crawl started", "job_id": "stub-job-id"}

@router.get("/status")
async def get_status():
    """Get crawler status"""
    return {"status": "idle", "last_run": None}

@router.get("/stats")
async def get_stats():
    """Get collection statistics"""
    return {"total_clinics": 0, "last_updated": None}

@router.get("/jobs")
async def get_jobs():
    """Get crawl job history"""
    return {"jobs": []}
