"""
Seed fake reviews into review_schema.reviews.
Usage: python -m data_collector_service.scripts.import_hotosm (or run this file directly)
"""
import uuid
import random
from datetime import datetime, timedelta

import psycopg2

# Review comments in Vietnamese
POSITIVE_COMMENTS = [
    "Bác sĩ tư vấn rất nhiệt tình, phòng khám sạch sẽ, nhân viên thân thiện.",
    "Được khám nhanh chóng, bác sĩ giỏi, có chuyên môn cao. Sẽ quay lại.",
    "Phòng khám hiện đại, bác sĩ kinh nghiệm, đáng tin cậy.",
    "Dịch vụ tốt, bác sĩ khám kỹ lưỡng, giải thích rõ ràng về bệnh.",
    "Nhân viên nhiệt tình, không phải chờ đợi lâu. Rất hài lòng!",
    "Bác sĩ chữa bệnh tốt, phòng khám gần nhà, tiện lợi.",
    "Quy trình khám nhanh gọn, bác sĩ chu đáo, cảm ơn bác sĩ!",
    "Cơ sở vật chất tốt, bác sĩ chuyên nghiệp, giá hợp lý.",
    "Đã khám và điều trị hiệu quả. Bác sĩ theo dõi sát sao.",
    "Phòng khám đáng đến, bác sĩ tận tâm với bệnh nhân.",
]

NEUTRAL_COMMENTS = [
    "Khám xong thì bình thường, bác sĩ đủ nhiệt tình.",
    "Phòng khám ổn, có thể cải thiện thêm về thời gian chờ.",
    "Bác sĩ khám đúng lúc, nhưng phòng hơi đông vào giờ cao điểm.",
    "Dịch vụ tạm được, nên đặt lịch trước để không phải chờ lâu.",
    "Cơ sở vật chất tốt nhưng thời gian chờ hơi lâu.",
    "Bác sĩ giỏi, nhưng nên liên hệ đặt lịch trước để tiết kiệm thời gian.",
]

REVIEWER_NAMES = [
    "Nguyễn Văn An", "Trần Thị Bình", "Lê Hoàng Cường", "Phạm Minh Đức",
    "Hoàng Thu Hà", "Vũ Thanh Lan", "Đặng Quốc Duy", "Bùi Thu Hương",
    "Cao Minh Khoa", "Đinh Thị Kim", "Phan Văn Lâm", "Trịnh Thị Mai",
    "Ngô Đức Nam", "Lương Thị Oanh", "Hồ Văn Phong", "Đào Thị Quỳnh",
    "Lý Minh Sơn", "Võ Thị Thanh", "Chu Văn Toàn", "Hà Thị Uyên",
]

PROS_TEMPLATES = [
    "Bác sĩ nhiệt tình, ", "Phòng khám sạch sẽ, ", "Nhân viên thân thiện, ",
    "Khám nhanh, ", "Vị trí thuận tiện, ", "Giá cả hợp lý, ",
    "Trang thiết bị hiện đại, ", "Lịch khám linh hoạt, ",
]

CONS_TEMPLATES = [
    "thời gian chờ hơi lâu", "phòng hơi nhỏ", "ít chỗ đỗ xe",
    "khó liên hệ đặt lịch", "giờ mở cửa hạn chế",
    "ca khám cuối hết sớm", "ít slot trống buổi chiều",
]


def _build_review(
    booking_id: uuid.UUID,
    user_id: uuid.UUID,
    clinic_id: uuid.UUID,
    doctor_id: uuid.UUID,
    days_ago: int,
    rating: int,
) -> dict:
    comment = random.choice(POSITIVE_COMMENTS) if rating >= 4 else random.choice(NEUTRAL_COMMENTS)
    num_pros = random.randint(1, 3)
    num_cons = random.randint(0, 2) if rating < 4 else 0
    pros = ", ".join(random.sample(PROS_TEMPLATES, num_pros)).rstrip(", ") + " " if num_pros else None
    cons = ", ".join(random.sample(CONS_TEMPLATES, num_cons)).rstrip(", ") if num_cons else None

    created_at = datetime.utcnow() - timedelta(days=days_ago)

    return {
        "id": str(uuid.uuid4()),
        "booking_id": str(booking_id),
        "user_id": str(user_id),
        "clinic_id": str(clinic_id),
        "doctor_id": str(doctor_id),
        "rating": rating,
        "comment": comment,
        "pros": pros,
        "cons": cons,
        "is_hidden": False,
        "created_at": created_at,
    }


def seed_reviews(limit_clinics: int = 500, reviews_per_clinic: int = 3):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
        options="-c search_path=review_schema,public",
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Check if we already have reviews
    cur.execute("SELECT COUNT(*) FROM reviews")
    existing = cur.fetchone()[0]
    if existing > 0:
        print(f"  reviews table already has {existing} rows — skipping.")
        cur.close()
        conn.close()
        return

    # Fetch existing doctors and clinics from clinic_schema
    cur.execute("""
        SELECT d.id, d.clinic_id, d.is_active
        FROM clinic_schema.doctors d
        WHERE d.is_active = true
        LIMIT %s
    """, (limit_clinics * 3,))
    doctors = cur.fetchall()

    if not doctors:
        print("  No active doctors found — skipping reviews seed.")
        cur.close()
        conn.close()
        return

    print(f"  Seeding reviews for up to {limit_clinics} clinics ({reviews_per_clinic} reviews each)...")

    inserted = 0
    clinic_ids_done = set()
    user_ids = [str(uuid.uuid4()) for _ in range(200)]
    booking_ids = [str(uuid.uuid4()) for _ in range(5000)]

    batch = []
    for doctor_id, clinic_id, *_ in doctors:
        clinic_id_str = str(clinic_id)
        if clinic_id_str in clinic_ids_done:
            continue
        clinic_ids_done.add(clinic_id_str)
        if len(clinic_ids_done) > limit_clinics:
            break

        for r in range(reviews_per_clinic):
            rating = random.choices([5, 4, 3], weights=[60, 30, 10])[0]
            days_ago = random.randint(1, 180)
            review = _build_review(
                booking_id=uuid.UUID(booking_ids.pop()),
                user_id=uuid.UUID(random.choice(user_ids)),
                clinic_id=uuid.UUID(clinic_id_str),
                doctor_id=uuid.UUID(str(doctor_id)),
                days_ago=days_ago,
                rating=rating,
            )
            batch.append(review)

    for review in batch:
        cur.execute("""
            INSERT INTO reviews (
                id, booking_id, user_id, clinic_id, doctor_id,
                rating, comment, pros, cons, is_hidden, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            review["id"],
            review["booking_id"],
            review["user_id"],
            review["clinic_id"],
            review["doctor_id"],
            review["rating"],
            review["comment"],
            review["pros"],
            review["cons"],
            review["is_hidden"],
            review["created_at"],
            review["created_at"],
        ))
        inserted += 1
        if inserted % 500 == 0:
            print(f"    {inserted} reviews inserted...")

    cur.close()
    conn.close()
    print(f"  Done! {inserted} fake reviews inserted into review_schema.reviews.")


if __name__ == "__main__":
    print("\n=== Seeding fake reviews ===")
    seed_reviews()
    print("=== Done ===\n")
