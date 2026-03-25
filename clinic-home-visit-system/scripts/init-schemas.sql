-- Database Initialization Script
-- Creates all schemas for the clinic home visit system

-- Auth Schema
CREATE SCHEMA IF NOT EXISTS auth_schema;

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

CREATE TABLE IF NOT EXISTS auth_schema.refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth_schema.users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Clinic Schema
CREATE SCHEMA IF NOT EXISTS clinic_schema;

CREATE TABLE IF NOT EXISTS clinic_schema.clinics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    lat DECIMAL(10, 8) NOT NULL,
    lng DECIMAL(11, 8) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    specialties TEXT[] NOT NULL,
    opening_time TIME NOT NULL,
    closing_time TIME NOT NULL,
    supports_home_visit BOOLEAN DEFAULT FALSE,
    home_visit_radius_km DECIMAL(5, 2) DEFAULT 10.0,
    min_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2),
    images TEXT[],
    owner_id UUID,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    data_source VARCHAR(20) DEFAULT 'manual',
    confidence_score DECIMAL(3, 2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

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

CREATE TABLE IF NOT EXISTS clinic_schema.doctor_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id UUID REFERENCES clinic_schema.doctors(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    slot_duration_minutes INTEGER DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE
);

-- Booking Schema
CREATE SCHEMA IF NOT EXISTS booking_schema;

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

-- Review Schema
CREATE SCHEMA IF NOT EXISTS review_schema;

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

-- Notification Schema
CREATE SCHEMA IF NOT EXISTS notification_schema;

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

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON auth_schema.users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON auth_schema.users(role);
CREATE INDEX IF NOT EXISTS idx_clinics_location ON clinic_schema.clinics(lat, lng);
CREATE INDEX IF NOT EXISTS idx_clinics_specialties ON clinic_schema.clinics USING GIN(specialties);
CREATE INDEX IF NOT EXISTS idx_doctors_clinic ON clinic_schema.doctors(clinic_id);
CREATE INDEX IF NOT EXISTS idx_doctors_specialty ON clinic_schema.doctors(specialty);
CREATE INDEX IF NOT EXISTS idx_bookings_user ON booking_schema.bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_bookings_clinic ON booking_schema.bookings(clinic_id);
CREATE INDEX IF NOT EXISTS idx_bookings_doctor ON booking_schema.bookings(doctor_id);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON booking_schema.bookings(status);
CREATE INDEX IF NOT EXISTS idx_bookings_scheduled ON booking_schema.bookings(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_reviews_clinic ON review_schema.reviews(clinic_id);
CREATE INDEX IF NOT EXISTS idx_reviews_doctor ON review_schema.reviews(doctor_id);
CREATE INDEX IF NOT EXISTS idx_reviews_booking ON review_schema.reviews(booking_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notification_schema.notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_status ON notification_schema.notifications(status);
