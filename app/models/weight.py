"""app/models/weight.py — Weight logs | Feature: Weight Tracker"""
from app.models.base_model import BaseModel


class WeightModel(BaseModel):
    TABLE = 'weight_logs'

    @classmethod
    def log(cls, uid, log_date, weight_kg, notes=''):
        return cls.execute(
            'INSERT INTO weight_logs(user_id,log_date,weight_kg,notes,created_at) '
            'VALUES(%s,%s,%s,%s,NOW()) '
            'ON DUPLICATE KEY UPDATE weight_kg=%s, notes=%s',
            (uid, log_date, weight_kg, notes, weight_kg, notes)
        )

    @classmethod
    def get_by_date(cls, uid, log_date):
        return cls.fetch_one(
            'SELECT * FROM weight_logs WHERE user_id=%s AND log_date=%s',
            (uid, log_date)
        )

    @classmethod
    def recent(cls, uid, limit=30):
        return cls.fetch_all(
            'SELECT * FROM weight_logs WHERE user_id=%s ORDER BY log_date DESC LIMIT %s',
            (uid, limit)
        )

    @classmethod
    def latest(cls, uid):
        return cls.fetch_one(
            'SELECT * FROM weight_logs WHERE user_id=%s ORDER BY log_date DESC LIMIT 1',
            (uid,)
        )

    @classmethod
    def delete(cls, wid, uid):
        return cls.execute(
            'DELETE FROM weight_logs WHERE id=%s AND user_id=%s', (wid, uid)
        )
