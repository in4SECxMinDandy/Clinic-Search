#!/usr/bin/env python3
"""
HOT-OSM Vietnam Health Facilities Import CLI
Run this script to import clinic data into the database.

Usage:
    python -m data_collector_service.scripts.import_hotosm [--include-pharmacies] [--include-hospitals] [--force]

Examples:
    python -m data_collector_service.scripts.import_hotosm
    python -m data_collector_service.scripts.import_hotosm --include-pharmacies
    python -m data_collector_service.scripts.import_hotosm --force
"""
import argparse
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from data_collector_service.hotosm_client import HotosmClient
from data_collector_service.utils.db import get_database

logger = structlog.get_logger()


async def import_facilities(
    session: AsyncSession,
    facilities: list,
    include_pharmacies: bool = False,
    include_hospitals: bool = False,
    force_update: bool = False,
) -> dict:
    """Import facilities into the database."""
    import uuid
    from datetime import time as dt_time

    DEFAULT_OPENING = dt_time(7, 0)
    DEFAULT_CLOSING = dt_time(18, 0)

    total_fetched = len(facilities)
    total_imported = 0
    total_updated = 0
    total_skipped = 0
    pharmacies_skipped = 0
    hospitals_skipped = 0

    for i, facility in enumerate(facilities):
        amenity_lower = (facility.amenity or "").lower()
        healthcare_lower = (facility.healthcare or "").lower()

        if amenity_lower == "pharmacy" or healthcare_lower == "pharmacy":
            pharmacies_skipped += 1
            if not include_pharmacies:
                total_skipped += 1
                continue

        if amenity_lower in ("hospital", "doctors") or healthcare_lower == "hospital":
            hospitals_skipped += 1
            if not include_hospitals:
                total_skipped += 1
                continue

        # Check if exists by name
        existing = None
        result = await session.execute(
            text(
                "SELECT id FROM clinic_schema.clinics "
                "WHERE data_source = 'hotosm' AND name = :name LIMIT 1"
            ),
            {"name": facility.display_name},
        )
        existing = result.scalar_one_or_none()

        if existing and not force_update:
            total_skipped += 1
            continue

        # Build address
        addr_parts = []
        if facility.address:
            addr_parts.append(facility.address)
        if facility.city:
            addr_parts.append(facility.city)
        addr_parts.append("Việt Nam")
        full_address = ", ".join(addr_parts)

        supports_home = amenity_lower == "clinic" or healthcare_lower == "clinic"

        if existing:
            await session.execute(
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
            clinic_id = str(uuid.uuid4())
            await session.execute(
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

        if (i + 1) % 500 == 0:
            logger.info("hotosm_import_progress", processed=i + 1, total=total_fetched)

    await session.commit()
    return {
        "total_fetched": total_fetched,
        "total_imported": total_imported,
        "total_updated": total_updated,
        "total_skipped": total_skipped,
        "pharmacies_skipped": pharmacies_skipped,
        "hospitals_skipped": hospitals_skipped,
    }


async def main():
    parser = argparse.ArgumentParser(
        description="Import HOT-OSM Vietnam health facilities into the database"
    )
    parser.add_argument(
        "--include-pharmacies",
        action="store_true",
        help="Include pharmacies in the import",
    )
    parser.add_argument(
        "--include-hospitals",
        action="store_true",
        help="Include hospitals in the import",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update existing records",
    )
    args = parser.parse_args()

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if sys.stdout.isatty() else structlog.processors.JSONRenderer(),
        ]
    )

    logger.info("hotosm_cli_started", args=args.model_dump())

    db = get_database()
    client = HotosmClient(timeout=120.0)

    logger.info("hotosm_fetching_data")
    facilities = await client.fetch_all()
    logger.info("hotosm_facilities_loaded", count=len(facilities))

    async with db.async_session_factory() as session:
        stats = await import_facilities(
            session,
            facilities,
            include_pharmacies=args.include_pharmacies,
            include_hospitals=args.include_hospitals,
            force_update=args.force,
        )

    logger.info("hotosm_import_completed", **stats)
    print(f"\n✅ Import hoàn tất!")
    print(f"   Tổng fetch: {stats['total_fetched']}")
    print(f"   Đã import: {stats['total_imported']}")
    print(f"   Đã update: {stats['total_updated']}")
    print(f"   Bỏ qua:   {stats['total_skipped']}")
    print(f"   (Nhà thuốc bỏ qua: {stats['pharmacies_skipped']})")
    print(f"   (Bệnh viện bỏ qua: {stats['hospitals_skipped']})")


if __name__ == "__main__":
    asyncio.run(main())
