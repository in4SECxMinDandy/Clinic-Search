"""
Clinic Service - SKILL.md

Skill cho Clinic Service - Quản lý phòng khám với GPS features.

## Nghiệp vụ chính
- CRUD phòng khám (tên, địa chỉ, chuyên khoa, giờ mở cửa, bác sĩ)
- Tìm kiếm theo tên, địa chỉ, chuyên khoa, đánh giá
- Lọc theo khoảng cách GPS, giá, chuyên khoa, thời gian mở cửa
- Xem chi tiết phòng khám (bác sĩ, dịch vụ, hình ảnh)
- Hỗ trợ khám tại nhà hay khám tại phòng khám
- Sắp xếp theo khoảng cách gần nhất từ vị trí user
- Lọc bán kính: hiển thị phòng khám trong N km
- Hiển thị khoảng cách từ user đến mỗi phòng khám

## Business Rules
- Phòng khám phải có tối thiểu: tên, địa chỉ, ít nhất 1 chuyên khoa
- Giờ mở cửa hợp lệ: 00:00 - 23:59
- Khoảng cách tính bằng Haversine formula từ GPS người dùng
- Chỉ hiển thị phòng khám đang hoạt động (không bị banned)
- Bán kính tìm kiếm mặc định: 10km, tối đa: 50km
- Mỗi response clinic bao gồm: distance_km (từ user), estimated_travel_time_min

## Database Schema (clinic_schema)
- clinics: id, name, address, lat, lng, phone, email, specialties, opening_time, closing_time
- doctors: id, clinic_id, name, specialty, license_number, experience_years, avatar, bio
- doctor_schedules: id, doctor_id, day_of_week, start_time, end_time, slot_duration_minutes

## GPS Features (shared/gps)
- Haversine distance calculation
- Nominatim geocoding
- OSRM routing (shortest path)
- Geofilter (points within radius)
"""

SERVICE_NAME = "clinic-service"
SERVICE_PORT = 8001
SCHEMA_NAME = "clinic_schema"
