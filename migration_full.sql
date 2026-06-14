-- BMI  CALCULATOR Records
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
