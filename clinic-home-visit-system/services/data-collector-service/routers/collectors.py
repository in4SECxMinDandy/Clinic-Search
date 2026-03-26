"""
Data Collector Service - Collectors Router
"""
import uuid
from datetime import time as dt_time
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from data_collector_service.hotosm_client import HotosmClient, HotosmFacility
from data_collector_service.utils.db import get_db_session

logger = structlog.get_logger()
router = APIRouter()

# Default working hours for imported facilities (no schedule data in HOT-OSM)
DEFAULT_OPENING = dt_time(7, 0)
DEFAULT_CLOSING = dt_time(18, 0)


class ImportRequest(BaseModel):
    include_pharmacies: bool = False
    include_hospitals: bool = False
    force_update: bool = False


class ImportStats(BaseModel):
    total_fetched: int
    total_imported: int
    total_skipped: int
    total_updated: int
    pharmacies_skipped: int
    hospitals_skipped: int


@router.post("/import/hotosm", response_model=ImportStats)
async def import_hotosm(
    request: ImportRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Download HOT-OSM Vietnam health facilities and import into the database.
    Only imports clinics/doctor offices by default (excludes pharmacies and hospitals).
    """
    logger.info("hotosm_import_started", request=request.model_dump())

    client = HotosmClient(timeout=120.0)
    facilities = await client.fetch_all()
    logger.info("hotosm_facilities_fetched", count=len(facilities))

    total_fetched = len(facilities)
    total_imported = 0
    total_updated = 0
    total_skipped = 0
    pharmacies_skipped = 0
    hospitals_skipped = 0

    for facility in facilities:
        # Filter by type
        amenity_lower = (facility.amenity or "").lower()
        healthcare_lower = (facility.healthcare or "").lower()

        if amenity_lower == "pharmacy" or healthcare_lower == "pharmacy":
            pharmacies_skipped += 1
            if not request.include_pharmacies:
                total_skipped += 1
                continue

        if amenity_lower in ("hospital", "doctors") or healthcare_lower == "hospital":
            hospitals_skipped += 1
            if not request.include_hospitals:
                total_skipped += 1
                continue

        # Check if already exists by OSM ID
        osm_id = facility.osm_id
        existing = None
        if osm_id:
            result = await db.execute(
                text(
                    "SELECT id FROM clinic_schema.clinics "
                    "WHERE data_source = 'hotosm' AND name = :name LIMIT 1"
                ),
                {"name": facility.display_name},
            )
            existing = result.scalar_one_or_none()

        if existing and not request.force_update:
            total_skipped += 1
            continue

        # Build address string
        addr_parts = []
        if facility.address:
            addr_parts.append(facility.address)
        if facility.city:
            addr_parts.append(facility.city)
        addr_parts.append("Việt Nam")
        full_address = ", ".join(addr_parts)

        # Determine if supports home visit (defaults based on amenity type)
        supports_home = amenity_lower == "clinic" or healthcare_lower == "clinic"

        if existing:
            # Update existing
            await db.execute(
                text(
                    "UPDATE clinic_schema.clinics SET "
                    "  address = :address, lat = :lat, lng = :lng, "
                    "  specialties = :specialties, supports_home_visit = :supports_home, "
                    "  updated_at = NOW() "
                    "WHERE id = :id"
                ),
                {
                    "address": full_address,
                    "lat": str(facility.lat),
                    "lng": str(facility.lng),
                    "specialties": facility.specialties,
                    "supports_home": supports_home,
                    "id": str(existing),
                },
            )
            total_updated += 1
        else:
            # Insert new
            clinic_id = str(uuid.uuid4())
            await db.execute(
                text(
                    "INSERT INTO clinic_schema.clinics "
                    "(id, name, address, lat, lng, specialties, "
                    " opening_time, closing_time, supports_home_visit, "
                    " data_source, is_active, is_verified, confidence_score) "
                    "VALUES "
                    "(:id, :name, :address, :lat, :lng, :specialties, "
                    " :opening, :closing, :supports_home, "
                    " 'hotosm', true, false, 0.7)"
                ),
                {
                    "id": clinic_id,
                    "name": facility.display_name,
                    "address": full_address,
                    "lat": str(facility.lat),
                    "lng": str(facility.lng),
                    "specialties": facility.specialties,
                    "opening": DEFAULT_OPENING,
                    "closing": DEFAULT_CLOSING,
                    "supports_home": supports_home,
                },
            )
            total_imported += 1

    await db.commit()
    logger.info(
        "hotosm_import_completed",
        total_fetched=total_fetched,
        imported=total_imported,
        updated=total_updated,
        skipped=total_skipped,
    )

    return ImportStats(
        total_fetched=total_fetched,
        total_imported=total_imported,
        total_updated=total_updated,
        total_skipped=total_skipped,
        pharmacies_skipped=pharmacies_skipped,
        hospitals_skipped=hospitals_skipped,
    )


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db_session)):
    """Get collection statistics from database."""
    result = await db.execute(
        text(
            "SELECT data_source, COUNT(*) as count "
            "FROM clinic_schema.clinics "
            "WHERE is_active = true "
            "GROUP BY data_source"
        )
    )
    rows = result.fetchall()

    total = await db.execute(
        text("SELECT COUNT(*) FROM clinic_schema.clinics WHERE is_active = true")
    )
    total_count = total.scalar()

    by_source = {row[0] or "manual": row[1] for row in rows}

    return {
        "total_clinics": total_count,
        "by_source": by_source,
    }


@router.get("/status")
async def get_status():
    """Get collector service status."""
    return {
        "status": "ready",
        "source": "hotosm_vnm_health_facilities",
        "dataset_url": "https://data.humdata.org/dataset/hotosm_vnm_health_facilities",
    }


@router.get("/jobs")
async def get_jobs():
    """Get crawl job history."""
    return {"jobs": []}
