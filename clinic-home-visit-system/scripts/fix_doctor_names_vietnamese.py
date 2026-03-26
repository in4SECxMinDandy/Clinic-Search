#!/usr/bin/env python3
"""
Repair doctor name/specialty/bio rows that were stored with ASCII '?' instead of Vietnamese UTF-8.

Run when Postgres is up (e.g. after docker-compose up):
  set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
  python scripts/fix_doctor_names_vietnamese.py

Requires: psycopg2-binary (same as clinic-service requirements).
"""
from __future__ import annotations

import os
import sys
import uuid as uuid_mod
from urllib.parse import urlparse

try:
    import psycopg2
except ImportError:
    print("Install psycopg2-binary: pip install psycopg2-binary", file=sys.stderr)
    sys.exit(1)

# Exact keys as stored when UTF-8 was lost (ASCII ? placeholders)
SPECIALTY_MAP: dict[str, str] = {
    "da li???u": "Da liễu",
    "h?? h???p": "Hô hấp",
    "m???t": "Mắt",
    "ngo???i khoa": "Ngoại khoa",
    "nhi khoa": "Nhi khoa",
    "n???i khoa": "Nội khoa",
    " r??ng h??m m???t": "Răng hàm mặt",
    "s???n ph??? khoa": "Sản phụ khoa",
    "tai m??i h???ng": "Tai mũi họng",
    "th???n kinh": "Thần kinh",
    "tim m???ch": "Tim mạch",
    "ti??u h??a": "Tiêu hóa",
}

STANDARD_BIO_VI = (
    "Bác sĩ có nhiều năm kinh nghiệm trong lĩnh vực chuyên khoa. "
    "Tốt nghiệp Đại học Y, đã tham gia nhiều khóa tập huấn chuyên sâu trong và ngoài nước."
)

SURNAMES = [
    "Nguyễn",
    "Trần",
    "Lê",
    "Phạm",
    "Hoàng",
    "Vũ",
    "Phan",
    "Đặng",
    "Đỗ",
    "Bùi",
    "Chu",
    "Ngô",
    "Hà",
    "Dương",
    "Võ",
]
MIDDLES = [
    "Văn",
    "Thị",
    "Đình",
    "Minh",
    "Thu",
    "Thanh",
    "Hoàng",
    "Quang",
    "Đức",
    "Ngọc",
    "Hữu",
    "Xuân",
]
GIVEN = [
    "An",
    "Bình",
    "Chi",
    "Dũng",
    "Hà",
    "Hào",
    "Huy",
    "Khôi",
    "Lan",
    "Linh",
    "Mai",
    "Minh",
    "Nam",
    "Phong",
    "Quang",
    "Sơn",
    "Tuấn",
    "Hương",
    "Thảo",
    "Hải",
    "Long",
    "Khoa",
]


def doctor_display_name(uid: str) -> str:
    u = uuid_mod.UUID(uid).int
    s = SURNAMES[u % len(SURNAMES)]
    m = MIDDLES[(u // 7) % len(MIDDLES)]
    g = GIVEN[(u // 13) % len(GIVEN)]
    return f"BS. {s} {m} {g}"


def needs_repair(text: str | None) -> bool:
    if not text:
        return False
    return "?" in text


def parse_database_url(url: str) -> dict:
    p = urlparse(url.replace("postgresql+asyncpg://", "postgresql://"))
    return {
        "host": p.hostname or "localhost",
        "port": p.port or 5432,
        "database": (p.path or "/postgres").lstrip("/") or "postgres",
        "user": p.username or "postgres",
        "password": p.password or "",
    }


def main() -> None:
    url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    cfg = parse_database_url(url)
    conn = psycopg2.connect(
        host=cfg["host"],
        port=cfg["port"],
        dbname=cfg["database"],
        user=cfg["user"],
        password=cfg["password"],
        client_encoding="UTF8",
    )
    conn.autocommit = False
    cur = conn.cursor()

    cur.execute(
        "SELECT id::text, name, specialty, bio FROM clinic_schema.doctors ORDER BY id"
    )
    rows = cur.fetchall()
    updated = 0
    for row_id, name, specialty, bio in rows:
        new_name = doctor_display_name(row_id) if needs_repair(name) else name
        new_spec = SPECIALTY_MAP.get(specialty, specialty)
        new_bio = STANDARD_BIO_VI if needs_repair(bio) else bio

        if (new_name, new_spec, new_bio) != (name, specialty, bio):
            cur.execute(
                """
                UPDATE clinic_schema.doctors
                SET name = %s, specialty = %s, bio = %s, updated_at = NOW()
                WHERE id = %s::uuid
                """,
                (new_name, new_spec, new_bio, row_id),
            )
            updated += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Updated {updated} doctor row(s) with repaired Vietnamese text.")


if __name__ == "__main__":
    main()
