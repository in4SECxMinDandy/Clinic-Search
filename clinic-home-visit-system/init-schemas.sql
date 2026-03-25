-- Initialize PostgreSQL schemas for multi-tenant microservices
-- This runs automatically on first start of postgres container

-- Create schemas for each service
CREATE SCHEMA IF NOT EXISTS auth_schema;
CREATE SCHEMA IF NOT EXISTS clinic_schema;
CREATE SCHEMA IF NOT EXISTS booking_schema;
CREATE SCHEMA IF NOT EXISTS review_schema;
CREATE SCHEMA IF NOT EXISTS notification_schema;

-- Grant permissions
GRANT ALL ON SCHEMA auth_schema TO postgres;
GRANT ALL ON SCHEMA clinic_schema TO postgres;
GRANT ALL ON SCHEMA booking_schema TO postgres;
GRANT ALL ON SCHEMA review_schema TO postgres;
GRANT ALL ON SCHEMA notification_schema TO postgres;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text matching

-- Auth Schema: Users table
CREATE TABLE IF NOT EXISTS auth_schema.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL DEFAULT 'patient',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified_at TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_auth_users_email ON auth_schema.users(email);
CREATE INDEX IF NOT EXISTS idx_auth_users_role ON auth_schema.users(role);

-- Auth Schema: User locations
CREATE TABLE IF NOT EXISTS auth_schema.user_locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth_schema.users(id) ON DELETE CASCADE,
    label VARCHAR(100),
    address TEXT NOT NULL,
    lat DECIMAL(10, 8) NOT NULL,
    lng DECIMAL(11, 8) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_locations_user ON auth_schema.user_locations(user_id);

-- Auth Schema: Refresh tokens
CREATE TABLE IF NOT EXISTS auth_schema.refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth_schema.users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user ON auth_schema.refresh_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_hash ON auth_schema.refresh_tokens(token_hash);

-- Clinic Schema: Clinics
CREATE TABLE IF NOT EXISTS clinic_schema.clinics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    lat DECIMAL(10, 8) NOT NULL,
    lng DECIMAL(11, 8) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    specialties TEXT[] NOT NULL DEFAULT '{}',
    opening_time TIME NOT NULL,
    closing_time TIME NOT NULL,
    supports_home_visit BOOLEAN DEFAULT FALSE,
    home_visit_radius_km DECIMAL(5, 2) DEFAULT 10.0,
    min_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2),
    images TEXT[] DEFAULT '{}',
    owner_id UUID,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    data_source VARCHAR(20) DEFAULT 'manual',
    confidence_score DECIMAL(3, 2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_clinics_lat_lng ON clinic_schema.clinics(lat, lng);
CREATE INDEX IF NOT EXISTS idx_clinics_active ON clinic_schema.clinics(is_active);
CREATE INDEX IF NOT EXISTS idx_clinics_specialties ON clinic_schema.clinics USING GIN(specialties);

-- Clinic Schema: Doctors
CREATE TABLE IF NOT EXISTS clinic_schema.doctors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_id UUID REFERENCES clinic_schema.clinics(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    license_number VARCHAR(50),
    experience_years INTEGER DEFAULT 0,
    avatar TEXT,
    bio TEXT,
    supports_home_visit BOOLEAN DEFAULT FALSE,
    available_home_visit_radius_km DECIMAL(5, 2) DEFAULT 5.0,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    rating DECIMAL(3, 2) DEFAULT 0.0,
    total_reviews INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_doctors_clinic ON clinic_schema.doctors(clinic_id);
CREATE INDEX IF NOT EXISTS idx_doctors_specialty ON clinic_schema.doctors(specialty);

-- Clinic Schema: Doctor schedules
CREATE TABLE IF NOT EXISTS clinic_schema.doctor_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID REFERENCES clinic_schema.doctors(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week >= 0 AND day_of_week <= 6),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    slot_duration_minutes INTEGER DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_doctor_schedules_doctor ON clinic_schema.doctor_schedules(doctor_id);

-- Booking Schema
CREATE TABLE IF NOT EXISTS booking_schema.bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    clinic_id UUID NOT NULL,
    doctor_id UUID NOT NULL,
    booking_type VARCHAR(20) NOT NULL,
    scheduled_at TIMESTAMP NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 30,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    home_address TEXT,
    home_lat DECIMAL(10, 8),
    home_lng DECIMAL(11, 8),
    notes TEXT,
    total_price DECIMAL(10, 2),
    payment_method VARCHAR(20),
    payment_status VARCHAR(20) DEFAULT 'unpaid',
    payment_transaction_id VARCHAR(100),
    cancellation_reason TEXT,
    cancelled_by VARCHAR(20),
    cancelled_at TIMESTAMP,
    confirmed_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_duration CHECK (duration_minutes >= 30 AND duration_minutes <= 120),
    CONSTRAINT valid_status CHECK (status IN ('pending', 'confirmed', 'in_progress', 'completed', 'cancelled', 'expired'))
);

CREATE INDEX IF NOT EXISTS idx_bookings_user ON booking_schema.bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_bookings_clinic ON booking_schema.bookings(clinic_id);
CREATE INDEX IF NOT EXISTS idx_bookings_doctor ON booking_schema.bookings(doctor_id);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON booking_schema.bookings(status);
CREATE INDEX IF NOT EXISTS idx_bookings_scheduled ON booking_schema.bookings(scheduled_at);

-- Booking Schema: Slots
CREATE TABLE IF NOT EXISTS booking_schema.booking_slots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID NOT NULL,
    slot_start TIMESTAMP NOT NULL,
    slot_end TIMESTAMP NOT NULL,
    booking_id UUID REFERENCES booking_schema.bookings(id),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(doctor_id, slot_start)
);

CREATE INDEX IF NOT EXISTS idx_booking_slots_doctor ON booking_schema.booking_slots(doctor_id);
CREATE INDEX IF NOT EXISTS idx_booking_slots_available ON booking_schema.booking_slots(is_available);

-- Review Schema
CREATE TABLE IF NOT EXISTS review_schema.reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID NOT NULL,
    user_id UUID NOT NULL,
    clinic_id UUID NOT NULL,
    doctor_id UUID NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    pros TEXT,
    cons TEXT,
    is_hidden BOOLEAN DEFAULT FALSE,
    hidden_reason VARCHAR(255),
    reply TEXT,
    replied_by UUID,
    replied_at TIMESTAMP,
    is_reported BOOLEAN DEFAULT FALSE,
    report_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reviews_clinic ON review_schema.reviews(clinic_id);
CREATE INDEX IF NOT EXISTS idx_reviews_doctor ON review_schema.reviews(doctor_id);
CREATE INDEX IF NOT EXISTS idx_reviews_booking ON review_schema.reviews(booking_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON review_schema.reviews(rating);

-- Review Schema: Reports
CREATE TABLE IF NOT EXISTS review_schema.review_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    review_id UUID REFERENCES review_schema.reviews(id) ON DELETE CASCADE,
    reporter_id UUID NOT NULL,
    reason VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_review_reports_review ON review_schema.review_reports(review_id);

-- Notification Schema
CREATE TABLE IF NOT EXISTS notification_schema.notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    type VARCHAR(50) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    recipient VARCHAR(255),
    subject VARCHAR(255),
    content TEXT NOT NULL,
    metadata JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notifications_user ON notification_schema.notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_status ON notification_schema.notifications(status);
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notification_schema.notifications(type);

-- Notification Schema: Email templates
CREATE TABLE IF NOT EXISTS notification_schema.email_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    subject_template VARCHAR(255) NOT NULL,
    body_template TEXT NOT NULL,
    variables JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Seed default email templates
INSERT INTO notification_schema.email_templates (code, subject_template, body_template, variables) VALUES
('booking_confirmation', 'Xác nhận đặt lịch khám #{{booking_id}}', 'Chào {{user_name}},\n\nLịch khám của bạn đã được xác nhận:\n- Phòng khám: {{clinic_name}}\n- Bác sĩ: {{doctor_name}}\n- Thời gian: {{scheduled_at}}\n- Địa điểm: {{address}}\n\nCảm ơn bạn đã sử dụng dịch vụ!', '["booking_id", "user_name", "clinic_name", "doctor_name", "scheduled_at", "address"]'),
('booking_reminder', 'Nhắc lịch khám ngày mai', 'Chào {{user_name}},\n\nNhắc nhở: Bạn có lịch khám vào ngày mai lúc {{scheduled_at}} tại {{clinic_name}}.\n\nVui lòng đến đúng giờ.', '["user_name", "scheduled_at", "clinic_name"]'),
('booking_cancelled', 'Thông báo hủy lịch khám', 'Chào {{user_name}},\n\nLịch khám #{{booking_id}} đã bị hủy.\nLý do: {{reason}}\n\nNếu bạn cần đặt lịch khác, vui lòng truy cập ứng dụng.', '["user_name", "booking_id", "reason"]'),
('review_request', 'Mời bạn đánh giá dịch vụ', 'Chào {{user_name}},\n\nCảm ơn bạn đã hoàn thành lịch khám tại {{clinic_name}}.\n\nHãy chia sẻ trải nghiệm của bạn để giúp những người khác có thêm thông tin.\n\nĐánh giá ngay: {{review_link}}', '["user_name", "clinic_name", "review_link"]')
ON CONFLICT (code) DO NOTHING;
