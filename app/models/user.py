"""app/models/user.py — User auth + profile | Feature: Registration/Login"""
from app.models.base_model import BaseModel
from app.auth import hash_password, verify_password


class UserModel(BaseModel):
    TABLE = 'users'

    @classmethod
    def create(cls, full_name, email, password):
        return cls.execute(
            'INSERT INTO users(full_name,email,password_hash,role,created_at) VALUES(%s,%s,%s,"user",NOW())',
            (full_name, email, hash_password(password))
        )

    @classmethod
    def find_by_email(cls, email):
        return cls.fetch_one('SELECT * FROM users WHERE email=%s LIMIT 1', (email,))

    @classmethod
    def find_by_id(cls, user_id):
        """Fetch a single user by primary key"""
        return cls.fetch_one('SELECT * FROM users WHERE id=%s LIMIT 1', (user_id,))

    @classmethod
    def authenticate(cls, email, password):
        u = cls.find_by_email(email)
        if u and verify_password(password, u['password_hash']):
            return u
        return None

    @classmethod
    def email_exists(cls, email) -> bool:
        return bool(cls.fetch_one('SELECT id FROM users WHERE email=%s LIMIT 1', (email,)))

    @classmethod
    def update_profile(cls, uid, full_name, phone, bio=''):
        """Update user profile: full_name, phone, bio"""
        return cls.execute(
            'UPDATE users SET full_name=%s, phone=%s, bio=%s, updated_at=NOW() WHERE id=%s',
            (full_name, phone, bio, uid)
        )

    @classmethod
    def update_phone(cls, uid, phone):
        """Update only phone number"""
        return cls.execute('UPDATE users SET phone=%s WHERE id=%s', (phone, uid))

    @classmethod
    def update_health(cls, uid, age, gender, weight_kg, height_cm, goal, activity):
        return cls.execute(
            'UPDATE users SET age=%s,gender=%s,weight_kg=%s,height_cm=%s,goal=%s,activity_level=%s WHERE id=%s',
            (age, gender, weight_kg, height_cm, goal, activity, uid)
        )

    @classmethod
    def update_password(cls, uid, new_pwd):
        return cls.execute(
            'UPDATE users SET password_hash=%s WHERE id=%s',
            (hash_password(new_pwd), uid)
        )

    @classmethod
    def get_all(cls):
        return cls.fetch_all(
            'SELECT id,full_name,email,role,created_at FROM users ORDER BY created_at DESC'
        )
    # ──────────────────────────────────────────────────────────────────────
    # ADMIN CONTROL PANEL METHODS
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def get_all_detailed(cls, search=''):
        if search:
            return cls.fetch_all(
                'SELECT id,full_name,email,role,phone,is_active,created_at,'
                'age,gender,weight_kg,height_cm,goal '
                'FROM users WHERE full_name LIKE %s OR email LIKE %s '
                'ORDER BY created_at DESC',
                (f'%{search}%', f'%{search}%')
            )
        return cls.fetch_all(
            'SELECT id,full_name,email,role,phone,is_active,created_at,'
            'age,gender,weight_kg,height_cm,goal '
            'FROM users ORDER BY created_at DESC'
        )

    @classmethod
    def count_all(cls):
        row = cls.fetch_one('SELECT COUNT(*) AS cnt FROM users')
        return int(row['cnt']) if row else 0

    @classmethod
    def count_active_today(cls):
        row = cls.fetch_one(
            "SELECT COUNT(DISTINCT user_id) AS cnt FROM calorie_logs WHERE log_date = CURDATE()"
        )
        return int(row['cnt']) if row else 0

    @classmethod
    def count_new_this_week(cls):
        row = cls.fetch_one(
            "SELECT COUNT(*) AS cnt FROM users WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)"
        )
        return int(row['cnt']) if row else 0

    @classmethod
    def admin_update(cls, uid, full_name, email, role, is_active):
        return cls.execute(
            'UPDATE users SET full_name=%s, email=%s, role=%s, is_active=%s WHERE id=%s',
            (full_name, email, role, is_active, uid)
        )

    @classmethod
    def set_active(cls, uid, is_active):
        return cls.execute('UPDATE users SET is_active=%s WHERE id=%s', (is_active, uid))

    @classmethod
    def admin_delete(cls, uid):
        # Clean up related records first (FK-safe deletion)
        tables = ['meals','calorie_logs','custom_foods','bmi_records','notifications',
                  'macro_targets','sleep_logs','mood_logs','weight_logs','workouts',
                  'medicines','medicine_logs','health_expenses','support_messages']
        for t in tables:
            try:
                cls.execute(f'DELETE FROM {t} WHERE user_id=%s', (uid,))
            except Exception:
                pass
        return cls.execute('DELETE FROM users WHERE id=%s', (uid,))

    @classmethod
    def get_admins(cls):
        return cls.fetch_all("SELECT id, email, full_name FROM users WHERE role='admin' AND is_active=1")
