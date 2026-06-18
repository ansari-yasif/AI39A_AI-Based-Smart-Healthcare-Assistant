"""app/models/mood.py — Mood logs | Feature: Mood Tracker"""
from app.models.base_model import BaseModel

class MoodModel(BaseModel):
    TABLE = 'mood_logs'

    @classmethod
    def log(cls, uid, date, mood, energy, notes=''):
        return cls.execute(
            'INSERT INTO mood_logs(user_id,log_date,mood,energy_level,notes,created_at) VALUES(%s,%s,%s,%s,%s,NOW()) '
            'ON DUPLICATE KEY UPDATE mood=%s,energy_level=%s,notes=%s,updated_at=NOW()',
            (uid,date,mood,energy,notes,mood,energy,notes))

    @classmethod
    def today(cls, uid, date):
        return cls.fetch_one('SELECT * FROM mood_logs WHERE user_id=%s AND log_date=%s',(uid,date))

    @classmethod
    def month(cls, uid, start, end):
        return cls.fetch_all(
            'SELECT * FROM mood_logs WHERE user_id=%s AND log_date BETWEEN %s AND %s ORDER BY log_date',
            (uid,start,end))

    @classmethod
    def frequency(cls, uid, start, end):
        return cls.fetch_all(
            'SELECT mood, COUNT(*) AS cnt FROM mood_logs WHERE user_id=%s AND log_date BETWEEN %s AND %s GROUP BY mood',
            (uid,start,end))

    @classmethod
    def get_by_date(cls, uid, date):
        return cls.fetch_one('SELECT * FROM mood_logs WHERE user_id=%s AND log_date=%s', (uid, date))

    @classmethod
    def recent(cls, uid, limit=14):
        return cls.fetch_all(
            'SELECT * FROM mood_logs WHERE user_id=%s ORDER BY log_date DESC LIMIT %s',
            (uid, limit)
        )
