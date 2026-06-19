-- =============================================================
-- VitaPulse — Complete Database Schema
-- Database: vitapulse_db
-- Run this file ONCE on a fresh database
-- =============================================================
 
CREATE DATABASE IF NOT EXISTS vitapulse_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
 
USE vitapulse_db;
 
-- =============================================================
-- 1. USERS
-- Core account table. Every other table references user_id.
-- =============================================================
CREATE TABLE IF NOT EXISTS users (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    full_name       VARCHAR(150) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    phone           VARCHAR(30),
    bio             TEXT,
    avatar_url      VARCHAR(500),
    role            VARCHAR(20) NOT NULL DEFAULT 'user'    COMMENT 'user | admin',
    is_active       TINYINT(1)  NOT NULL DEFAULT 1         COMMENT '0=deactivated by admin',
    -- Health profile (filled from Settings page)
    age             INT UNSIGNED,
    gender          VARCHAR(10)                            COMMENT 'male | female | other',
    weight_kg       FLOAT,
    height_cm       FLOAT,
    goal            VARCHAR(20)                            COMMENT 'lose | gain | maintain',
    activity_level  FLOAT       DEFAULT 1.55               COMMENT 'PAL multiplier: 1.2 sedentary → 1.9 very active',
    -- OAuth
    google_id       VARCHAR(100),
    created_at      DATETIME    DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email   (email),
    INDEX idx_users_role    (role),
    INDEX idx_users_active  (is_active)
);
 
-- =============================================================
-- 2. NUTRITION — Calorie Logs
-- One row per user per day, tracks total consumed vs goal.
-- =============================================================
CREATE TABLE IF NOT EXISTS calorie_logs (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id             INT UNSIGNED NOT NULL,
    log_date            DATE         NOT NULL,
    calories_consumed   FLOAT        NOT NULL DEFAULT 0,
    calorie_goal        FLOAT        NOT NULL DEFAULT 2000,
    created_at          DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_callog_user_date (user_id, log_date),
    INDEX idx_cl_user (user_id)
);
 
-- =============================================================
-- 3. NUTRITION — Meals
-- Individual food items logged per day.
-- =============================================================
CREATE TABLE IF NOT EXISTS meals (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    food_name   VARCHAR(255) NOT NULL,
    meal_type   ENUM('Breakfast','Lunch','Dinner','Snack') DEFAULT 'Snack',
    calories    FLOAT        NOT NULL DEFAULT 0,
    protein_g   FLOAT        NOT NULL DEFAULT 0,
    carbs_g     FLOAT        NOT NULL DEFAULT 0,
    fat_g       FLOAT        NOT NULL DEFAULT 0,
    log_date    DATE         NOT NULL,
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_meal_user_date (user_id, log_date)
);
 
-- =============================================================
-- 4. NUTRITION — Custom Foods
-- User-created food items for the food database.
-- =============================================================
CREATE TABLE IF NOT EXISTS custom_foods (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    name        VARCHAR(255) NOT NULL,
    calories    FLOAT        NOT NULL DEFAULT 0,
    protein_g   FLOAT        NOT NULL DEFAULT 0,
    carbs_g     FLOAT        NOT NULL DEFAULT 0,
    fat_g       FLOAT        NOT NULL DEFAULT 0,
    category    VARCHAR(100)          DEFAULT 'Custom',
    created_at  DATETIME              DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cf_user (user_id)
);
 
-- =============================================================
-- 5. NUTRITION — Macro Targets
-- Per-day macro & calorie goals set by the user.
-- =============================================================
CREATE TABLE IF NOT EXISTS macro_targets (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    target_date     DATE         NOT NULL,
    protein_target  FLOAT                 DEFAULT 0,
    carbs_target    FLOAT                 DEFAULT 0,
    fat_target      FLOAT                 DEFAULT 0,
    calorie_target  FLOAT                 DEFAULT 2000,
    created_at      DATETIME              DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME              DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_macro_user_date (user_id, target_date),
    INDEX idx_macro_user (user_id)
);
 
-- =============================================================
-- 6. HEALTH — BMI Records
-- Persistent BMI history from the BMI Calculator.
-- =============================================================
CREATE TABLE IF NOT EXISTS bmi_records (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    weight_kg   FLOAT        NOT NULL,
    height_cm   FLOAT        NOT NULL,
    bmi_value   FLOAT        NOT NULL,
    bmi_label   VARCHAR(50)           COMMENT 'Underweight | Normal | Overweight | Obese',
    bmi_color   VARCHAR(20)           DEFAULT '#22c55e',
    recorded_at DATE         NOT NULL DEFAULT (CURRENT_DATE),
    created_at  DATETIME              DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_bmi_user_date (user_id, recorded_at)
);
 
-- =============================================================
-- 7. HEALTH — Sleep Tracker
-- One row per user per night.
-- =============================================================
CREATE TABLE IF NOT EXISTS sleep_logs (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    log_date      DATE         NOT NULL,
    bedtime       TIME,
    wake_time     TIME,
    hours_slept   FLOAT,
    quality       TINYINT               DEFAULT 3  COMMENT '1=Poor 2=Fair 3=Good 4=Great 5=Excellent',
    notes         TEXT,
    created_at    DATETIME              DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME              DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_sleep_user_date (user_id, log_date),
    INDEX idx_sleep_user (user_id)
);
 
-- =============================================================
-- 8. HEALTH — Mood Tracker
-- One row per user per day.
-- =============================================================
CREATE TABLE IF NOT EXISTS mood_logs (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    log_date      DATE         NOT NULL,
    mood          VARCHAR(30)  NOT NULL  COMMENT 'happy|sad|energetic|calm|stressed|tired|focused|anxious|excited|angry',
    energy_level  TINYINT               DEFAULT 3  COMMENT '1-5 scale',
    notes         TEXT,
    created_at    DATETIME              DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME              DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_mood_user_date (user_id, log_date),
    INDEX idx_mood_user (user_id)
);
 
-- =============================================================
-- 9. HEALTH — Weight Tracker
-- One row per user per day.
-- =============================================================
CREATE TABLE IF NOT EXISTS weight_logs (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    log_date      DATE         NOT NULL,
    weight_kg     FLOAT        NOT NULL,
    notes         TEXT,
    created_at    DATETIME              DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_weight_user_date (user_id, log_date),
    INDEX idx_weight_user (user_id)
);
 
-- =============================================================
-- 10. HEALTH — Workouts
-- Individual workout sessions.
-- =============================================================
CREATE TABLE IF NOT EXISTS workouts (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    workout_type    VARCHAR(50),
    duration_min    INT                  DEFAULT 0,
    calories_burned INT                  DEFAULT 0,
    notes           TEXT,
    log_date        DATE         NOT NULL,
    created_at      DATETIME             DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_workout_user (user_id),
    INDEX idx_workout_date (user_id, log_date)
);
 
-- =============================================================
-- 11. WELLNESS — Notifications
-- In-app notifications for user events.
-- =============================================================
CREATE TABLE IF NOT EXISTS notifications (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    title       VARCHAR(255) NOT NULL,
    body        TEXT,
    type        VARCHAR(50)           DEFAULT 'info'  COMMENT 'info | success | warning | health',
    is_read     TINYINT(1)            DEFAULT 0,
    link        VARCHAR(255),
    created_at  DATETIME              DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notif_user   (user_id),
    INDEX idx_notif_unread (user_id, is_read)
);
 
-- =============================================================
-- 12. WELLNESS — Medicine Reminders
-- User's active medicines with scheduled reminder times.
-- =============================================================
CREATE TABLE IF NOT EXISTS medicines (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    name          VARCHAR(150) NOT NULL,
    dosage        VARCHAR(100),
    times         VARCHAR(255) NOT NULL  COMMENT 'comma-separated HH:MM values e.g. 08:00,14:00,21:00',
    frequency     VARCHAR(50)            DEFAULT 'daily'  COMMENT 'daily | weekly | as-needed',
    start_date    DATE,
    end_date      DATE,
    notes         TEXT,
    active        TINYINT(1)             DEFAULT 1,
    created_at    DATETIME               DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_med_user (user_id)
);
 
-- =============================================================
-- 13. WELLNESS — Medicine Dose Logs
-- Tracks which scheduled doses were taken/missed.
-- =============================================================
CREATE TABLE IF NOT EXISTS medicine_logs (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    medicine_id     INT UNSIGNED NOT NULL,
    user_id         INT UNSIGNED NOT NULL,
    log_date        DATE         NOT NULL,
    scheduled_time  VARCHAR(10)           COMMENT 'e.g. 08:00',
    status          VARCHAR(20)           DEFAULT 'taken'  COMMENT 'taken | missed | snoozed',
    taken_at        DATETIME              DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_medlog_user_date (user_id, log_date),
    INDEX idx_medlog_med       (medicine_id)
);
 
-- =============================================================
-- 14. WELLNESS — Health Expense Tracker
-- User's health-related spending records.
-- =============================================================
CREATE TABLE IF NOT EXISTS health_expenses (
    id              INT UNSIGNED   AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED   NOT NULL,
    category        VARCHAR(50)    NOT NULL  COMMENT 'Medicine|Doctor Visit|Lab Test|Hospital|Insurance|Supplements|Other',
    amount          DECIMAL(10,2)  NOT NULL,
    description     VARCHAR(255),
    expense_date    DATE           NOT NULL,
    created_at      DATETIME                 DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_exp_user_date (user_id, expense_date)
);
 
-- =============================================================
-- 15. WELLNESS — Support Messages (User → Admin)
-- Messages sent by users to the admin team.
-- =============================================================
CREATE TABLE IF NOT EXISTS support_messages (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNSIGNED NOT NULL,
    subject       VARCHAR(255) NOT NULL,
    message       TEXT         NOT NULL,
    status        VARCHAR(20)           DEFAULT 'open'  COMMENT 'open | replied | closed',
    admin_reply   TEXT,
    replied_at    DATETIME,
    created_at    DATETIME              DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_support_user   (user_id),
    INDEX idx_support_status (status)
);
 
-- =============================================================
-- 16. WELLNESS — Outbreak Alerts (Admin → All Users)
-- Admins create these; they show as a banner on every dashboard.
-- =============================================================
CREATE TABLE IF NOT EXISTS outbreak_alerts (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(255) NOT NULL,
    description   TEXT,
    severity      VARCHAR(20)           DEFAULT 'medium'  COMMENT 'low | medium | high | critical',
    region        VARCHAR(150),
    active        TINYINT(1)            DEFAULT 1,
    created_at    DATETIME              DEFAULT CURRENT_TIMESTAMP,
    expires_at    DATETIME,
    INDEX idx_outbreak_active (active)
);
 
-- =============================================================
-- 17. SYSTEM — Site Settings
-- Key-value config used by the AI chatbot for contact info.
-- =============================================================
CREATE TABLE IF NOT EXISTS site_settings (
    setting_key     VARCHAR(100) PRIMARY KEY,
    setting_value   VARCHAR(500)
);