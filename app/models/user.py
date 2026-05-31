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
    def authenticate(cls, email, password):
        u = cls.find_by_email(email)
        if u and verify_password(password, u['password_hash']):
            return u
        return None

    @classmethod
    def email_exists(cls, email) -> bool:
        return bool(cls.fetch_one('SELECT id FROM users WHERE email=%s LIMIT 1', (email,)))

    @classmethod
    def update_profile(cls, uid, full_name, bio=''):
        return cls.execute(
            'UPDATE users SET full_name=%s,bio=%s,updated_at=NOW() WHERE id=%s',
            (full_name, bio, uid)
        )

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
