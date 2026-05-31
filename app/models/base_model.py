"""app/models/base_model.py — Shared DB access for all models"""
from app.models.database import db


class BaseModel:
    TABLE: str = ''

    @classmethod
    def execute(cls, sql, params=()):
        return db.execute(sql, params)

    @classmethod
    def fetch_one(cls, sql, params=()):
        return db.fetch_one(sql, params)

    @classmethod
    def fetch_all(cls, sql, params=()):
        return db.fetch_all(sql, params)

    @classmethod
    def find_by_id(cls, rid: int):
        return cls.fetch_one(f'SELECT * FROM {cls.TABLE} WHERE id=%s LIMIT 1', (rid,))

    @classmethod
    def delete_by_id(cls, rid: int):
        return cls.execute(f'DELETE FROM {cls.TABLE} WHERE id=%s', (rid,))
