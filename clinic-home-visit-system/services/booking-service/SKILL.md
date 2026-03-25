"""
Booking Service - SKILL.md

Skill cho Booking Service - Quản lý đặt lịch khám.

## Nghiệp vụ chính
- Tạo booking (chọn phòng khám, bác sĩ, thời gian, loại khám)
- Cập nhật trạng thái booking (pending → confirmed → completed/cancelled)
- Xem lịch sử booking của user
- Hủy booking (chỉ khi trạng thái pending hoặc confirmed, hủy trước 2 tiếng)
- Thông báo khi có thay đổi trạng thái

## Business Rules
- Không cho đặt quá khứ
- Mỗi bác sĩ chỉ 1 booking mỗi slot 30 phút
- Khám tại nhà: bác sĩ phải hỗ trợ home visit
- Thanh toán: thanh toán tại nhà hoặc chuyển khoản trước
- Booking confirmed tự động hết hạn sau 24h nếu không thanh toán
- Thời gian khám tối thiểu 30 phút, tối đa 120 phút

## Database Schema (booking_schema)
- bookings: id, user_id, clinic_id, doctor_id, booking_type, scheduled_at, status, home_address
- booking_slots: id, doctor_id, slot_start, slot_end, booking_id, is_available

## Inter-service Events
- booking.created → notification-service
- booking.confirmed → notification-service
- booking.completed → notification-service, review-service
- booking.cancelled → notification-service
"""

SERVICE_NAME = "booking-service"
SERVICE_PORT = 8002
SCHEMA_NAME = "booking_schema"
