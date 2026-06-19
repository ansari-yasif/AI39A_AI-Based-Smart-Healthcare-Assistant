-- =============================================================
-- VitaPulse — Seed Data
-- Run this AFTER schema.sql
-- Populates demo data so every feature is visible immediately
-- =============================================================
 
USE vitapulse_db;
 
-- =============================================================
-- USERS
-- Admin password : Admin@123
-- Demo password  : Demo@1234
-- Passwords are bcrypt hashes — do NOT change by hand here.
-- To change a password, use the Settings page after login,
-- or run: UPDATE users SET password_hash = '<new_hash>' WHERE email = '...';
-- =============================================================
INSERT INTO users
    (full_name, email, password_hash, phone, role, is_active,
     age, gender, weight_kg, height_cm, goal, activity_level, created_at)
VALUES
-- Admin account  (password: Admin@123)
(
    'Admin VitaPulse',
    'admin@vitapulse.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaJqMQyBDpGJ6JhIQF4x2Bz5u',
    '+977 9800000001',
    'admin', 1,
    30, 'male', 72.0, 175.0, 'maintain', 1.55,
    NOW() - INTERVAL 90 DAY
),
-- Regular demo user  (password: Demo@1234)
(
    'Ansar Khan',
    'ansar@demo.com',
    '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uJTgENEm2',
    '+977 9800000002',
    'user', 1,
    24, 'male', 68.5, 172.0, 'lose', 1.375,
    NOW() - INTERVAL 30 DAY
),
-- Second demo user
(
    'Priya Sharma',
    'priya@demo.com',
    '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uJTgENEm2',
    '+977 9800000003',
    'user', 1,
    22, 'female', 55.0, 162.0, 'maintain', 1.55,
    NOW() - INTERVAL 15 DAY
)
ON DUPLICATE KEY UPDATE full_name = VALUES(full_name);
 
-- =============================================================
-- CALORIE LOGS  (14 days for demo user id=2)
-- =============================================================
INSERT INTO calorie_logs (user_id, log_date, calories_consumed, calorie_goal) VALUES
(2, CURDATE() - INTERVAL 13 DAY, 1820, 1900),
(2, CURDATE() - INTERVAL 12 DAY, 2050, 1900),
(2, CURDATE() - INTERVAL 11 DAY, 1750, 1900),
(2, CURDATE() - INTERVAL 10 DAY, 1980, 1900),
(2, CURDATE() - INTERVAL  9 DAY, 1650, 1900),
(2, CURDATE() - INTERVAL  8 DAY, 2100, 1900),
(2, CURDATE() - INTERVAL  7 DAY, 1870, 1900),
(2, CURDATE() - INTERVAL  6 DAY, 1920, 1900),
(2, CURDATE() - INTERVAL  5 DAY, 1780, 1900),
(2, CURDATE() - INTERVAL  4 DAY, 2200, 1900),
(2, CURDATE() - INTERVAL  3 DAY, 1850, 1900),
(2, CURDATE() - INTERVAL  2 DAY, 1960, 1900),
(2, CURDATE() - INTERVAL  1 DAY, 1730, 1900),
(2, CURDATE(),                   1450, 1900)
ON DUPLICATE KEY UPDATE calories_consumed = VALUES(calories_consumed);
 
-- =============================================================
-- MEALS  (today for demo user)
-- =============================================================
INSERT INTO meals (user_id, food_name, meal_type, calories, protein_g, carbs_g, fat_g, log_date) VALUES
(2, 'Oatmeal with banana',      'Breakfast', 350, 12,  60, 6,  CURDATE()),
(2, 'Boiled eggs (2)',          'Breakfast', 140, 12,  1,  10, CURDATE()),
(2, 'Dal Bhat (1 plate)',       'Lunch',     520, 22,  80, 10, CURDATE()),
(2, 'Mixed vegetable salad',    'Lunch',     120, 4,   18, 3,  CURDATE()),
(2, 'Apple',                    'Snack',     80,  0.4, 21, 0.2,CURDATE()),
(2, 'Almonds (20g)',            'Snack',     120, 4,   4,  10, CURDATE()),
(2, 'Chicken curry with rice',  'Dinner',    580, 35,  65, 14, CURDATE()),
(2, 'Yogurt (150g)',            'Dinner',    90,  8,   10, 2,  CURDATE());
 
-- =============================================================
-- CUSTOM FOODS
-- =============================================================
INSERT INTO custom_foods (user_id, name, calories, protein_g, carbs_g, fat_g, category) VALUES
(2, 'Dal Bhat (home)',       480, 20, 75,  8,  'Local Food'),
(2, 'Sel Roti (1 piece)',    220, 4,  40,  6,  'Local Food'),
(2, 'Momo (6 pieces)',       320, 18, 35,  10, 'Local Food'),
(2, 'Lassi (1 glass)',       180, 8,  28,  4,  'Beverages')
ON DUPLICATE KEY UPDATE calories = VALUES(calories);
 
-- =============================================================
-- BMI RECORDS  (3 months history for demo user)
-- =============================================================
INSERT INTO bmi_records (user_id, weight_kg, height_cm, bmi_value, bmi_label, bmi_color, recorded_at) VALUES
(2, 72.0, 172.0, 24.3, 'Normal',     '#22c55e', CURDATE() - INTERVAL 90 DAY),
(2, 70.5, 172.0, 23.8, 'Normal',     '#22c55e', CURDATE() - INTERVAL 60 DAY),
(2, 69.2, 172.0, 23.4, 'Normal',     '#22c55e', CURDATE() - INTERVAL 30 DAY),
(2, 68.5, 172.0, 23.2, 'Normal',     '#22c55e', CURDATE()),
(3, 55.0, 162.0, 20.9, 'Normal',     '#22c55e', CURDATE() - INTERVAL 15 DAY),
(3, 54.8, 162.0, 20.9, 'Normal',     '#22c55e', CURDATE());
 
-- =============================================================
-- MACRO TARGETS
-- =============================================================
INSERT INTO macro_targets (user_id, target_date, protein_target, carbs_target, fat_target, calorie_target) VALUES
(2, CURDATE(), 130, 200, 55, 1900),
(3, CURDATE(), 100, 220, 60, 2000)
ON DUPLICATE KEY UPDATE calorie_target = VALUES(calorie_target);
 
-- =============================================================
-- SLEEP LOGS  (14 days for demo user)
-- =============================================================
INSERT INTO sleep_logs (user_id, log_date, bedtime, wake_time, hours_slept, quality, notes) VALUES
(2, CURDATE() - INTERVAL 13 DAY, '22:30', '06:30', 8.0, 4, 'Slept well'),
(2, CURDATE() - INTERVAL 12 DAY, '23:15', '07:00', 7.8, 3, NULL),
(2, CURDATE() - INTERVAL 11 DAY, '00:00', '07:30', 7.5, 3, 'Stayed up late'),
(2, CURDATE() - INTERVAL 10 DAY, '22:00', '06:00', 8.0, 5, 'Best sleep this week'),
(2, CURDATE() - INTERVAL  9 DAY, '23:45', '06:45', 7.0, 3, NULL),
(2, CURDATE() - INTERVAL  8 DAY, '22:30', '05:30', 7.0, 2, 'Woke up early'),
(2, CURDATE() - INTERVAL  7 DAY, '21:30', '06:00', 8.5, 5, 'Great sleep'),
(2, CURDATE() - INTERVAL  6 DAY, '23:00', '07:00', 8.0, 4, NULL),
(2, CURDATE() - INTERVAL  5 DAY, '23:30', '06:30', 7.0, 3, NULL),
(2, CURDATE() - INTERVAL  4 DAY, '22:45', '06:45', 8.0, 4, NULL),
(2, CURDATE() - INTERVAL  3 DAY, '23:00', '07:00', 8.0, 3, NULL),
(2, CURDATE() - INTERVAL  2 DAY, '22:00', '06:30', 8.5, 5, 'Excellent'),
(2, CURDATE() - INTERVAL  1 DAY, '23:15', '07:15', 8.0, 4, NULL),
(2, CURDATE(),                   '22:30', '06:30', 8.0, 4, 'Feeling rested')
ON DUPLICATE KEY UPDATE hours_slept = VALUES(hours_slept);
 
-- =============================================================
-- MOOD LOGS  (14 days)
-- =============================================================
INSERT INTO mood_logs (user_id, log_date, mood, energy_level, notes) VALUES
(2, CURDATE() - INTERVAL 13 DAY, 'happy',    4, 'Great start'),
(2, CURDATE() - INTERVAL 12 DAY, 'calm',     3, NULL),
(2, CURDATE() - INTERVAL 11 DAY, 'tired',    2, 'Long day'),
(2, CURDATE() - INTERVAL 10 DAY, 'energetic',5, 'Gym day!'),
(2, CURDATE() - INTERVAL  9 DAY, 'focused',  4, NULL),
(2, CURDATE() - INTERVAL  8 DAY, 'stressed', 2, 'Work pressure'),
(2, CURDATE() - INTERVAL  7 DAY, 'happy',    5, 'Weekend'),
(2, CURDATE() - INTERVAL  6 DAY, 'calm',     4, NULL),
(2, CURDATE() - INTERVAL  5 DAY, 'energetic',4, NULL),
(2, CURDATE() - INTERVAL  4 DAY, 'focused',  3, NULL),
(2, CURDATE() - INTERVAL  3 DAY, 'happy',    4, 'Good mood'),
(2, CURDATE() - INTERVAL  2 DAY, 'calm',     4, NULL),
(2, CURDATE() - INTERVAL  1 DAY, 'energetic',4, NULL),
(2, CURDATE(),                   'happy',    4, 'Feeling great today')
ON DUPLICATE KEY UPDATE mood = VALUES(mood);
 
-- =============================================================
-- WEIGHT LOGS  (14 days)
-- =============================================================
INSERT INTO weight_logs (user_id, log_date, weight_kg, notes) VALUES
(2, CURDATE() - INTERVAL 13 DAY, 69.8, 'Morning weight'),
(2, CURDATE() - INTERVAL 12 DAY, 69.5, NULL),
(2, CURDATE() - INTERVAL 11 DAY, 69.7, NULL),
(2, CURDATE() - INTERVAL 10 DAY, 69.2, 'After gym'),
(2, CURDATE() - INTERVAL  9 DAY, 69.4, NULL),
(2, CURDATE() - INTERVAL  8 DAY, 69.0, NULL),
(2, CURDATE() - INTERVAL  7 DAY, 68.8, 'Good week'),
(2, CURDATE() - INTERVAL  6 DAY, 69.1, NULL),
(2, CURDATE() - INTERVAL  5 DAY, 68.9, NULL),
(2, CURDATE() - INTERVAL  4 DAY, 68.7, NULL),
(2, CURDATE() - INTERVAL  3 DAY, 68.6, NULL),
(2, CURDATE() - INTERVAL  2 DAY, 68.5, NULL),
(2, CURDATE() - INTERVAL  1 DAY, 68.4, NULL),
(2, CURDATE(),                   68.5, 'Stable')
ON DUPLICATE KEY UPDATE weight_kg = VALUES(weight_kg);
 
-- =============================================================
-- WORKOUTS  (last 10 sessions)
-- =============================================================
INSERT INTO workouts (user_id, workout_type, duration_min, calories_burned, notes, log_date) VALUES
(2, 'Running',       30, 280, '5km run',          CURDATE() - INTERVAL 12 DAY),
(2, 'Gym / Weights', 45, 220, 'Chest & back day',  CURDATE() - INTERVAL 11 DAY),
(2, 'Cycling',       40, 260, 'Morning ride',      CURDATE() - INTERVAL  9 DAY),
(2, 'HIIT',          20, 200, '20-min HIIT',       CURDATE() - INTERVAL  8 DAY),
(2, 'Yoga',          45, 120, 'Evening yoga',      CURDATE() - INTERVAL  7 DAY),
(2, 'Running',       35, 310, '6km easy run',      CURDATE() - INTERVAL  5 DAY),
(2, 'Gym / Weights', 50, 240, 'Legs day',          CURDATE() - INTERVAL  4 DAY),
(2, 'Walking',       45, 150, 'Brisk walk',        CURDATE() - INTERVAL  2 DAY),
(2, 'HIIT',          20, 190, 'Morning HIIT',      CURDATE() - INTERVAL  1 DAY),
(2, 'Gym / Weights', 40, 210, 'Shoulders & arms',  CURDATE());
 
-- =============================================================
-- NOTIFICATIONS
-- =============================================================
INSERT INTO notifications (user_id, title, body, type, is_read, link) VALUES
(2, 'Welcome to VitaPulse! 🎉',    'Start by filling in your health profile in Settings.', 'success', 0, '/profile/settings'),
(2, 'BMI Logged ✓',                'Your BMI of 23.2 is in the Normal range. Keep it up!',  'info',    0, '/nutrition/bmi'),
(2, 'Weekly Report Ready 📊',      'Your weekly nutrition and health report is ready.',       'info',    1, '/nutrition/reports'),
(2, 'Medicine reminder set: Vitamin D 💊', 'Scheduled at 08:00',                             'health',  0, '/wellness/medicine');
 
-- =============================================================
-- MEDICINES  (demo reminders)
-- =============================================================
INSERT INTO medicines (user_id, name, dosage, times, frequency, start_date, notes, active) VALUES
(2, 'Vitamin D3',    '1 capsule',  '08:00',       'daily',     CURDATE() - INTERVAL 7 DAY, 'Take with breakfast', 1),
(2, 'Omega-3',       '2 capsules', '08:00,21:00', 'daily',     CURDATE() - INTERVAL 5 DAY, 'Take with food',      1),
(2, 'Paracetamol',   '500mg',      '08:00,14:00,21:00', 'as-needed', CURDATE(),             'Only if needed',      1);
 
-- =============================================================
-- HEALTH EXPENSES  (last 30 days)
-- =============================================================
INSERT INTO health_expenses (user_id, category, amount, description, expense_date) VALUES
(2, 'Medicine',      350.00, 'Vitamin D3 & Omega-3',         CURDATE() - INTERVAL 25 DAY),
(2, 'Doctor Visit',  800.00, 'General checkup - Dr. Sharma', CURDATE() - INTERVAL 20 DAY),
(2, 'Lab Test',      1200.00,'Blood test - lipid profile',   CURDATE() - INTERVAL 18 DAY),
(2, 'Supplements',   450.00, 'Whey protein (1kg)',           CURDATE() - INTERVAL 15 DAY),
(2, 'Medicine',      120.00, 'Paracetamol strips',           CURDATE() - INTERVAL 10 DAY),
(2, 'Doctor Visit',  600.00, 'Follow-up consultation',       CURDATE() - INTERVAL  5 DAY),
(2, 'Supplements',   380.00, 'Multivitamins (30 tabs)',      CURDATE() - INTERVAL  2 DAY),
(2, 'Lab Test',       950.00,'Vitamin D blood test',         CURDATE() - INTERVAL  1 DAY);
 
-- =============================================================
-- SUPPORT MESSAGES  (one demo message)
-- =============================================================
INSERT INTO support_messages (user_id, subject, message, status, admin_reply, replied_at) VALUES
(2,
'Question about calorie tracking',
'Hi, I wanted to ask how the calorie goal is calculated. Is it based on my BMR?',
'replied',
'Hi Ansar! Yes, your calorie goal is calculated from your BMR using the Mifflin-St Jeor formula, then multiplied by your activity level (TDEE). You can update your activity level in Health Settings to get a more accurate goal. Let us know if you have more questions!',
NOW() - INTERVAL 2 DAY
),
(2,
'Feature request: Dark mode toggle',
'Would love a toggle to switch between dark and light mode. The current dark theme is great though!',
'open',
NULL,
NULL
);
 
-- =============================================================
-- OUTBREAK ALERTS  (1 active demo alert)
-- =============================================================
INSERT INTO outbreak_alerts (title, description, severity, region, active) VALUES
(
    'Dengue Fever Alert',
    'An increase in dengue cases has been reported in the Kathmandu Valley. Use mosquito repellent, wear long sleeves, and eliminate standing water near your home. Seek medical attention immediately if you develop high fever, severe headache, or rash.',
    'medium',
    'Kathmandu Valley, Nepal',
    1
),
(
    'Seasonal Flu Advisory',
    'Influenza activity is elevated this season. The Health Ministry recommends getting vaccinated, frequent handwashing, and staying home if symptomatic.',
    'low',
    'Nepal (Nationwide)',
    1
);
 
-- =============================================================
-- SITE SETTINGS  (for AI chatbot contact info)
-- =============================================================
INSERT INTO site_settings (setting_key, setting_value) VALUES
    ('contact_address', 'Kathmandu, Putalisadak'),
    ('contact_phone',   '+977 9765682939'),
    ('contact_email',   'vitapulse123@gmail.com'),
    ('app_name',        'VitaPulse'),
    ('app_tagline',     'Your Complete Health & Wellness Platform')
ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value);
 
-- =============================================================
-- MAKE ADMIN  (sets the admin@vitapulse.com to role=admin)
-- This runs last to ensure the user exists first
-- =============================================================
UPDATE users SET role = 'admin', is_active = 1
WHERE email = 'admin@vitapulse.com';