"""app/models/sleep.py — Sleep logs | Feature: Sleep Tracker"""
from app.models.base_model import BaseModel

class SleepModel(BaseModel):
    TABLE = 'sleep_logs'

    @classmethod
    def log(cls, uid, date, bedtime, wake, hours, quality, notes=''):
        return cls.execute(
            'INSERT INTO sleep_logs(user_id,log_date,bedtime,wake_time,hours_slept,quality,notes,created_at) VALUES(%s,%s,%s,%s,%s,%s,%s,NOW()) '
            'ON DUPLICATE KEY UPDATE bedtime=%s,wake_time=%s,hours_slept=%s,quality=%s,notes=%s,updated_at=NOW()',
            (uid,date,bedtime,wake,hours,quality,notes,bedtime,wake,hours,quality,notes))

    @classmethod
    def today(cls, uid, date):
        return cls.fetch_one('SELECT * FROM sleep_logs WHERE user_id=%s AND log_date=%s',(uid,date))

    @classmethod
    def week(cls, uid, start, end):
        return cls.fetch_all(
            'SELECT * FROM sleep_logs WHERE user_id=%s AND log_date BETWEEN %s AND %s ORDER BY log_date',
            (uid,start,end))

    @classmethod
    def avg_hours(cls, uid, start, end) -> float:
        row = cls.fetch_one(
            'SELECT AVG(hours_slept) AS avg_h FROM sleep_logs WHERE user_id=%s AND log_date BETWEEN %s AND %s',
            (uid,start,end))
        if not row or row.get('avg_h') is None: return 0.0
        return round(float(row['avg_h']),1)

    @classmethod
    def get_by_date(cls, uid, date):
        return cls.fetch_one('SELECT * FROM sleep_logs WHERE user_id=%s AND log_date=%s', (uid, date))

    @classmethod
    def recent(cls, uid, limit=14):
        return cls.fetch_all(
            'SELECT * FROM sleep_logs WHERE user_id=%s ORDER BY log_date DESC LIMIT %s',
            (uid, limit)
        )

    @classmethod
    def delete(cls, sid, uid):
        return cls.execute('DELETE FROM sleep_logs WHERE id=%s AND user_id=%s', (sid, uid))
