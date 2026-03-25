"""
Auth Service - SKILL.md

Skill cho Auth Service - Xác thực và phân quyền người dùng.

## Nghiệp vụ chính
- Đăng ký / Đăng nhập (email + password)
- JWT token authentication với access/refresh token
- Phân quyền: patient, doctor, admin, clinic_owner
- Quản lý profile (thông tin cá nhân, địa chỉ, SĐT)
- Đổi mật khẩu, quên mật khẩu (email OTP)

## Business Rules
- Email phải unique, format hợp lệ
- Password tối thiểu 8 ký tự, có chữ hoa, chữ thường, số
- JWT access token: 15 phút, refresh token: 7 ngày
- Refresh token chỉ dùng 1 lần (rotation)
- Account bị khóa sau 5 lần đăng nhập thất bại

## Database Schema (auth_schema)
- users: id, email, password_hash, full_name, phone, role, is_active
- user_locations: id, user_id, address, lat, lng, is_default
- refresh_tokens: id, user_id, token_hash, expires_at, is_revoked

## Dependencies
- shared.database.Database
- shared.redis_client.RedisClient
- passlib[bcrypt] cho password hashing
- python-jose[cryptography] cho JWT

## Environment Variables
- DATABASE_URL
- REDIS_URL
- JWT_SECRET
- JWT_ALGORITHM (default: HS256)
- ACCESS_TOKEN_EXPIRE_MINUTES (default: 15)
- REFRESH_TOKEN_EXPIRE_DAYS (default: 7)
- MAX_LOGIN_ATTEMPTS (default: 5)
- LOCKOUT_DURATION_MINUTES (default: 30)
"""

# Auth Service Configuration
SERVICE_NAME = "auth-service"
SERVICE_PORT = 8003
SCHEMA_NAME = "auth_schema"
