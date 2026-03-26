-- Update doctor ratings and reviews from existing data
UPDATE clinic_schema.doctors
SET
    rating = ROUND((RANDOM() * 1.5 + 3.5)::numeric, 1),
    total_reviews = (RANDOM() * 100 + 5)::int,
    bio = 'Bác sĩ có nhiều năm kinh nghiệm trong lĩnh vực chuyên khoa. Tốt nghiệp Đại học Y, đã tham gia nhiều khóa tập huấn chuyên sâu trong và ngoài nước.'
WHERE is_active = true;

-- Add doctor schedules (Mon-Sat, 7:00-18:00)
DO $$
DECLARE
    doc RECORD;
BEGIN
    FOR doc IN SELECT id FROM clinic_schema.doctors LOOP
        FOR day IN 0..5 LOOP
            INSERT INTO clinic_schema.doctor_schedules (id, doctor_id, day_of_week, start_time, end_time, slot_duration_minutes, is_active)
            VALUES (
                gen_random_uuid(),
                doc.id,
                day,
                '07:00:00'::time,
                '18:00:00'::time,
                30,
                true
            );
        END LOOP;
    END LOOP;
END $$;

SELECT 'Schedules added: ' || COUNT(*) FROM clinic_schema.doctor_schedules;
SELECT 'Doctors with updated ratings: ' || COUNT(*) FROM clinic_schema.doctors;
