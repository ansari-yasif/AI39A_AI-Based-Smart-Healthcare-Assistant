-- migration_nutrition.sql
-- Run this ONCE against your vitapulse_db database to add nutrition tables

-- Custom foods created by users
CREATE TABLE IF NOT EXISTS custom_foods (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    name        VARCHAR(255) NOT NULL,
    calories    FLOAT NOT NULL DEFAULT 0,
    protein_g   FLOAT NOT NULL DEFAULT 0,
    carbs_g     FLOAT NOT NULL DEFAULT 0,
    fat_g       FLOAT NOT NULL DEFAULT 0,
    category    VARCHAR(100) DEFAULT 'Custom',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cf_user (user_id)
);

-- Ensure calorie_logs table exists (may already exist)
CREATE TABLE IF NOT EXISTS calorie_logs (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id             INT UNSIGNED NOT NULL,
    log_date            DATE NOT NULL,
    calories_consumed   FLOAT NOT NULL DEFAULT 0,
    calorie_goal        FLOAT NOT NULL DEFAULT 2000,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_user_date (user_id, log_date),
    INDEX idx_cl_user (user_id)
);

-- Ensure meals table exists (may already exist)
CREATE TABLE IF NOT EXISTS meals (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    food_name   VARCHAR(255) NOT NULL,
    meal_type   ENUM('Breakfast','Lunch','Dinner','Snack') DEFAULT 'Snack',
    calories    FLOAT NOT NULL DEFAULT 0,
    protein_g   FLOAT NOT NULL DEFAULT 0,
    carbs_g     FLOAT NOT NULL DEFAULT 0,
    fat_g       FLOAT NOT NULL DEFAULT 0,
    log_date    DATE NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_m_user_date (user_id, log_date)
);

-- BMI Records table (optional persistent storage - app uses session by default)
CREATE TABLE IF NOT EXISTS bmi_records (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    weight_kg   FLOAT NOT NULL,
    height_cm   FLOAT NOT NULL,
    bmi_value   FLOAT NOT NULL,
    bmi_label   VARCHAR(50),
    recorded_at DATE DEFAULT (CURRENT_DATE),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_bmi_user (user_id)
);

-- BMI Records persistent storage (replaces session-only storage)
CREATE TABLE IF NOT EXISTS bmi_records (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    weight_kg   FLOAT NOT NULL,
    height_cm   FLOAT NOT NULL,
    bmi_value   FLOAT NOT NULL,
    bmi_label   VARCHAR(50),
    bmi_color   VARCHAR(20),
    recorded_at DATE NOT NULL DEFAULT (CURRENT_DATE),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_bmi_user_date (user_id, recorded_at)
);

-- Notifications table
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
    INDEX idx_notif_read (user_id, is_read)
);

-- Macro targets (user-customized per-day targets)
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
    mood          VARCHAR(30) NOT NULL COMMENT 'happy/sad/energetic/calm/stressed/tired/focused/anxious',
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
    INDEX idx_weight_user (user_id),
    UNIQUE KEY uq_weight_user_date (user_id, log_date)
);

-- Workouts
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
