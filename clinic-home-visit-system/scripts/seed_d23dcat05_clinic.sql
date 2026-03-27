-- Seed script for D23DCAT05 Clinic and Owner Account
-- Run: docker exec -i postgres psql -U postgres -d postgres < scripts/seed_d23dcat05_clinic.sql

-- Create owner user (clinic_owner role)
-- Password: D23DCAT05@2026 (bcrypt hash)
INSERT INTO auth_schema.users (
    id,
    email,
    password_hash,
    full_name,
    phone,
    role,
    is_active,
    failed_login_attempts,
    created_at,
    updated_at
) VALUES (
    '839dc620-64d4-4320-b7d3-bd81fccb724a',
    'owner_d23dcat05@clinic.vn',
    '$2b$12$ZQ3ANuU2Wko9Uvv4IAsZveyGA..KcCjARz/mUrnCX5jasBk7c.iKS',
    'Chu So Huu D23DCAT05',
    '0912345678',
    'clinic_owner',
    true,
    0,
    NOW(),
    NOW()
) ON CONFLICT (email) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    phone = EXCLUDED.phone,
    role = 'clinic_owner',
    is_active = true,
    updated_at = NOW();

-- Create clinic
INSERT INTO clinic_schema.clinics (
    id,
    name,
    address,
    lat,
    lng,
    phone,
    email,
    specialties,
    opening_time,
    closing_time,
    supports_home_visit,
    home_visit_radius_km,
    min_price,
    max_price,
    images,
    owner_id,
    is_active,
    is_verified,
    data_source,
    confidence_score,
    created_at,
    updated_at
) VALUES (
    'ab28f7d0-e5f3-4611-b2bf-5147954d9fae',
    'Phong Kham D23DCAT05',
    '122 Hoang Quoc Viet, Cau Giay, Ha Noi',
    21.0367,
    105.7873,
    '02412345678',
    'contact_d23dcat05@clinic.vn',
    ARRAY['general'],
    '08:00:00',
    '17:00:00',
    true,
    15.0,
    150000.0,
    500000.0,
    ARRAY['https://images.unsplash.com/photo-1629909613654-28e377c37b09?w=800&q=80'],
    '839dc620-64d4-4320-b7d3-bd81fccb724a',
    true,
    true,
    'manual',
    1.0,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Create sample doctor for the clinic
INSERT INTO clinic_schema.doctors (
    id,
    clinic_id,
    name,
    specialty,
    license_number,
    experience_years,
    avatar,
    bio,
    supports_home_visit,
    available_home_visit_radius_km,
    is_verified,
    is_active,
    rating,
    total_reviews,
    created_at,
    updated_at
) VALUES (
    '2439f2c5-a725-43ba-a05b-a9b762298ae5',
    'ab28f7d0-e5f3-4611-b2bf-5147954d9fae',
    'Bac Si Nguyen Van A',
    'general',
    'PK-2024-001',
    10,
    'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400&q=80',
    'Bac si chuyen khoa da khoa voi 10 nam kinh nghiem, dam bao chat luong kham chua tot.',
    true,
    10.0,
    true,
    true,
    4.5,
    25,
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;

-- Create doctor schedule (Mon-Fri, 8:00-17:00)
INSERT INTO clinic_schema.doctor_schedules (
    doctor_id,
    day_of_week,
    start_time,
    end_time,
    slot_duration_minutes,
    is_active
) VALUES
    ('2439f2c5-a725-43ba-a05b-a9b762298ae5', 1, '08:00:00', '17:00:00', 30, true),
    ('2439f2c5-a725-43ba-a05b-a9b762298ae5', 2, '08:00:00', '17:00:00', 30, true),
    ('2439f2c5-a725-43ba-a05b-a9b762298ae5', 3, '08:00:00', '17:00:00', 30, true),
    ('2439f2c5-a725-43ba-a05b-a9b762298ae5', 4, '08:00:00', '17:00:00', 30, true),
    ('2439f2c5-a725-43ba-a05b-a9b762298ae5', 5, '08:00:00', '17:00:00', 30, true)
ON CONFLICT DO NOTHING;

-- Verify data
SELECT 'Owner User:' as info;
SELECT id, email, full_name, role, is_active FROM auth_schema.users WHERE email = 'owner_d23dcat05@clinic.vn';

SELECT 'Clinic:' as info;
SELECT id, name, address, lat, lng, owner_id, supports_home_visit FROM clinic_schema.clinics WHERE name = 'Phong Kham D23DCAT05';

SELECT 'Doctors:' as info;
SELECT id, name, specialty, clinic_id FROM clinic_schema.doctors WHERE clinic_id = 'ab28f7d0-e5f3-4611-b2bf-5147954d9fae';
