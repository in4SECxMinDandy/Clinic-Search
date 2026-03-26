"""
HOT-OSM Vietnam Health Facilities Client
Download and parse GeoJSON from HDX S3 bucket.
"""
import io
import json
import zipfile
from dataclasses import dataclass
from datetime import time
from typing import Optional

import httpx
import structlog

logger = structlog.get_logger()


# Direct S3 URLs for Vietnam health facilities (points = clinics/hospitals, polygons = buildings)
HOTOSM_VNM_POINTS_URL = (
    "https://s3.dualstack.us-east-1.amazonaws.com/"
    "production-raw-data-api/ISO3/VNM/health_facilities/points/"
    "hotosm_vnm_health_facilities_points_geojson.zip"
)

HOTOSM_VNM_POLYGONS_URL = (
    "https://s3.dualstack.us-east-1.amazonaws.com/"
    "production-raw-data-api/ISO3/VNM/health_facilities/polygons/"
    "hotosm_vnm_health_facilities_polygons_geojson.zip"
)


@dataclass
class HotosmFacility:
    """Parsed facility from HOT-OSM GeoJSON."""
    name: str
    name_vi: Optional[str]
    name_en: Optional[str]
    amenity: Optional[str]
    healthcare: Optional[str]
    specialty: Optional[str]
    operator_type: Optional[str]
    capacity: Optional[str]
    address: Optional[str]
    city: Optional[str]
    lat: float
    lng: float
    osm_id: Optional[int]
    osm_type: Optional[str]
    source: Optional[str]

    @property
    def display_name(self) -> str:
        return self.name_vi or self.name_en or self.name or "Không tên"

    @property
    def display_address(self) -> str:
        parts = []
        if self.address:
            parts.append(self.address)
        if self.city:
            parts.append(self.city)
        parts.append("Việt Nam")
        return ", ".join(parts) or "Việt Nam"

    @property
    def specialties(self) -> list[str]:
        result = []
        if self.amenity and self.amenity not in ("", "yes"):
            result.append(self.amenity)
        if self.healthcare and self.healthcare not in ("", "yes"):
            result.append(self.healthcare)
        if self.specialty:
            for s in self.specialty.split(";"):
                s = s.strip()
                if s:
                    result.append(s)
        return result if result else ["y_tế"]

    def is_clinic_like(self) -> bool:
        """Return True if this facility is a clinic/doctor office (not a pharmacy or hospital ward)."""
        amenity_lower = (self.amenity or "").lower()
        healthcare_lower = (self.healthcare or "").lower()
        exclude = {"pharmacy", "hospital", "doctors", "dentist"}
        return amenity_lower not in exclude and healthcare_lower not in exclude


class HotosmClient:
    """Client for downloading and parsing HOT-OSM Vietnam health facilities data."""

    def __init__(self, timeout: float = 60.0):
        self.timeout = timeout

    async def _fetch_zip(self, url: str) -> Optional[bytes]:
        """Download ZIP file from URL."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info("hotosm_fetching", url=url)
                response = await client.get(url)
                response.raise_for_status()
                logger.info("hotosm_fetched", url=url, size=len(response.content))
                return response.content
        except httpx.HTTPStatusError as e:
            logger.error("hotosm_http_error", url=url, status=e.response.status_code)
            return None
        except Exception as e:
            logger.error("hotosm_fetch_error", url=url, error=str(e))
            return None

    async def _parse_zip(self, data: bytes, zip_name: str) -> list[HotosmFacility]:
        """Parse GeoJSON from ZIP bytes."""
        facilities = []
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                for name in zf.namelist():
                    if name.endswith(".geojson"):
                        content = zf.read(name)
                        geojson = json.loads(content)
                        facilities.extend(self._parse_geojson(geojson))
                        logger.info("hotosm_parsed", file=name, count=len(geojson.get("features", [])))
                        break
        except zipfile.BadZipFile:
            logger.error("hotosm_bad_zip", source=zip_name)
        except Exception as e:
            logger.error("hotosm_parse_error", source=zip_name, error=str(e))
        return facilities

    def _parse_geojson(self, geojson: dict) -> list[HotosmFacility]:
        """Parse GeoJSON FeatureCollection into HotosmFacility list."""
        facilities = []
        features = geojson.get("features", [])
        for feature in features:
            props = feature.get("properties", {}) or {}
            geom = feature.get("geometry", {}) or {}
            coords = geom.get("coordinates", [])

            # Points: [lng, lat]; Polygons: [[[lng, lat, ...]]]
            if geom.get("type") == "Point":
                lng, lat = coords[0], coords[1]
            elif geom.get("type") == "Polygon" and coords:
                # Use centroid of first ring
                ring = coords[0]
                lng = sum(c[0] for c in ring) / len(ring)
                lat = sum(c[1] for c in ring) / len(ring)
            else:
                continue

            # Extract name (prefer Vietnamese, then English, then OSM name)
            name = props.get("name") or props.get("name:vi") or props.get("name:en") or ""
            name_vi = props.get("name:vi") or props.get("name")
            name_en = props.get("name:en")

            facility = HotosmFacility(
                name=name,
                name_vi=name_vi,
                name_en=name_en,
                amenity=props.get("amenity"),
                healthcare=props.get("healthcare"),
                specialty=props.get("healthcare:speciality"),
                operator_type=props.get("operator:type"),
                capacity=props.get("capacity:persons"),
                address=props.get("addr:full"),
                city=props.get("addr:city"),
                lat=lat,
                lng=lng,
                osm_id=props.get("osm_id"),
                osm_type=props.get("osm_type"),
                source=props.get("source"),
            )
            facilities.append(facility)
        return facilities

    async def fetch_all(self) -> list[HotosmFacility]:
        """Fetch both points and polygons, deduplicate by OSM ID."""
        all_facilities: dict[int, HotosmFacility] = {}

        # Fetch points
        data = await self._fetch_zip(HOTOSM_VNM_POINTS_URL)
        if data:
            for f in await self._parse_zip(data, "points"):
                if f.osm_id:
                    all_facilities[f.osm_id] = f

        # Fetch polygons
        data = await self._fetch_zip(HOTOSM_VNM_POLYGONS_URL)
        if data:
            for f in await self._parse_zip(data, "polygons"):
                if f.osm_id and f.osm_id not in all_facilities:
                    all_facilities[f.osm_id] = f

        logger.info("hotosm_total", total=len(all_facilities))
        return list(all_facilities.values())
