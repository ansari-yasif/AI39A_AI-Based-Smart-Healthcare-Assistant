CREATE TABLE IF NOT EXISTS workouts (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    workout_type VARCHAR(50),
    duration_min INT DEFAULT 0,
    calories_burned INT DEFAULT 0,
    notes TEXT,
    log_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_workout_user (user_id)
);
