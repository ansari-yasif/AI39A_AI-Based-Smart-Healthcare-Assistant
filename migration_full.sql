-- =============================================================
-- VitaPulse — Full Database Migration
-- Run this file once to create all tables
-- =============================================================

-- Custom foods
CREATE TABLE IF NOT EXISTS custom_foods (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    name        VARCHAR(255) NOT NULL,
    calories    FLOAT DEFAULT 0,
    protein_g   FLOAT DEFAULT 0,
    carbs_g     FLOAT DEFAULT 0,
    fat_g       FLOAT DEFAULT 0,
    category    VARCHAR(100) DEFAULT 'Custom',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cf_user (user_id)
);

-- Calorie logs
CREATE TABLE IF NOT EXISTS calorie_logs (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id             INT UNSIGNED NOT NULL,
    log_date            DATE NOT NULL,
    calories_consumed   INT DEFAULT 0,
    calorie_goal        INT DEFAULT 2000,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_callog_user_date (user_id, log_date)
);

-- Meals
CREATE TABLE IF NOT EXISTS meals (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    food_name   VARCHAR(255),
    meal_type   VARCHAR(50) DEFAULT 'Snack',
    calories    FLOAT DEFAULT 0,
    protein_g   FLOAT DEFAULT 0,
    carbs_g     FLOAT DEFAULT 0,
    fat_g       FLOAT DEFAULT 0,
    log_date    DATE NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_meal_user_date (user_id, log_date)
);

-- BMI Records
CREATE TABLE IF NOT EXISTS bmi_records (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    weight_kg   FLOAT NOT NULL,
    height_cm   FLOAT NOT NULL,
    bmi_value   FLOAT NOT NULL,
    bmi_label   VARCHAR(50),
    bmi_color   VARCHAR(20) DEFAULT '#22c55e',
    recorded_at DATE NOT NULL DEFAULT (CURRENT_DATE),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_bmi_user_date (user_id, recorded_at)
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    title       VARCHAR(255) NOT NULL,
    body        TEXT,
    type        VARCHAR(50) DEFAULT 'info',
    is_read     TINYINT(1) DEFAULT 0,
    link        VARCHAR(255) DEFAULT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notif_user (user_id),
    INDEX idx_notif_unread (user_id, is_read)
);

-- Macro targets
CREATE TABLE IF NOT EXISTS macro_targets (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    target_date     DATE NOT NULL,
    protein_target  FLOAT DEFAULT 0,
    carbs_target    FLOAT DEFAULT 0,
    fat_target      FLOAT DEFAULT 0,
    calorie_target  FLOAT DEFAULT 2000,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_macro_user_date (user_id, target_date)
);

-- Sleep Tracker
CREATE TABLE IF NOT EXISTS sleep_logs (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    log_date      DATE NOT NULL,
    bedtime       TIME,
    wake_time     TIME,
    hours_slept   FLOAT,
    quality       TINYINT DEFAULT 3 COMMENT '1=Poor 2=Fair 3=Good 4=Great 5=Excellent',
    notes         TEXT,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_sleep_user_date (user_id, log_date),
    INDEX idx_sleep_user (user_id)
);

-- Mood Tracker
CREATE TABLE IF NOT EXISTS mood_logs (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    log_date      DATE NOT NULL,
    mood          VARCHAR(30) NOT NULL,
    energy_level  TINYINT DEFAULT 3 COMMENT '1-5 scale',
    notes         TEXT,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_mood_user_date (user_id, log_date),
    INDEX idx_mood_user (user_id)
);

-- Weight Tracker
CREATE TABLE IF NOT EXISTS weight_logs (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    log_date      DATE NOT NULL,
    weight_kg     FLOAT NOT NULL,
    notes         TEXT,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_weight_user_date (user_id, log_date),
    INDEX idx_weight_user (user_id)
);

-- Workout Tracker
CREATE TABLE IF NOT EXISTS workouts (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    workout_type    VARCHAR(50),
    duration_min    INT DEFAULT 0,
    calories_burned INT DEFAULT 0,
    notes           TEXT,
    log_date        DATE NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_workout_user (user_id)
);

-- Add bmi_color if not already present (safe alter)
ALTER TABLE bmi_records ADD COLUMN IF NOT EXISTS bmi_color VARCHAR(20) DEFAULT '#22c55e';

-- =============================================================
-- v8 ADDITIONS — Wellness features (Medicine, Expenses, Support,
-- Outbreak Alerts) + Site Settings (for AI chatbot contact info)
-- =============================================================

-- Medicine Reminders
CREATE TABLE IF NOT EXISTS medicines (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    name          VARCHAR(150) NOT NULL,
    dosage        VARCHAR(100),
    times         VARCHAR(255) NOT NULL COMMENT 'comma-separated HH:MM list e.g. 08:00,14:00,21:00',
    frequency     VARCHAR(50) DEFAULT 'daily',
    start_date    DATE,
    end_date      DATE,
    notes         TEXT,
    active        TINYINT(1) DEFAULT 1,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_med_user (user_id)
);

CREATE TABLE IF NOT EXISTS medicine_logs (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    medicine_id   INT UNSIGNED NOT NULL,
    user_id       INT UNSIGNED NOT NULL,
    taken_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    log_date      DATE NOT NULL,
    scheduled_time VARCHAR(10),
    status        VARCHAR(20) DEFAULT 'taken' COMMENT 'taken/missed/snoozed',
    INDEX idx_medlog_user_date (user_id, log_date)
);

-- Health Expense Tracker
CREATE TABLE IF NOT EXISTS health_expenses (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    category      VARCHAR(50) NOT NULL COMMENT 'Medicine/Doctor Visit/Lab Test/Hospital/Insurance/Supplements/Other',
    amount        DECIMAL(10,2) NOT NULL,
    description   VARCHAR(255),
    expense_date  DATE NOT NULL,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_exp_user_date (user_id, expense_date)
);

-- Contact / Support Messages to Admin
CREATE TABLE IF NOT EXISTS support_messages (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    subject       VARCHAR(255) NOT NULL,
    message       TEXT NOT NULL,
    status        VARCHAR(20) DEFAULT 'open' COMMENT 'open/replied/closed',
    admin_reply   TEXT,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    replied_at    DATETIME,
    INDEX idx_support_user (user_id),
    INDEX idx_support_status (status)
);

-- Outbreak Alerts (admin-managed, shown on all dashboards)
CREATE TABLE IF NOT EXISTS outbreak_alerts (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(255) NOT NULL,
    description   TEXT,
    severity      VARCHAR(20) DEFAULT 'medium' COMMENT 'low/medium/high/critical',
    region        VARCHAR(150),
    active        TINYINT(1) DEFAULT 1,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at    DATETIME
);

-- Site Settings (used by AI chatbot for contact info)
CREATE TABLE IF NOT EXISTS site_settings (
    setting_key   VARCHAR(100) PRIMARY KEY,
    setting_value VARCHAR(500)
);

INSERT INTO site_settings (setting_key, setting_value) VALUES
    ('contact_address', 'Kathmandu, Putalisadak'),
    ('contact_phone', '+977 9765682939'),
    ('contact_email', 'vitapulse123@gmail.com')
ON DUPLICATE KEY UPDATE setting_value = setting_value;

-- Ensure users table has is_active for admin panel
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active TINYINT(1) DEFAULT 1;
