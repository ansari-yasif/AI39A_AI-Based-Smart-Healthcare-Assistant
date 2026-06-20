"""app/models/calorie.py — Calorie logs | Feature: Calorie Tracker"""
from app.models.base_model import BaseModel

class CalorieModel(BaseModel):
    TABLE = 'calorie_logs'

    @classmethod
    def log(cls, uid, date, calories, goal):
        return cls.execute(
            'INSERT INTO calorie_logs(user_id,log_date,calories_consumed,calorie_goal) VALUES(%s,%s,%s,%s) '
            'ON DUPLICATE KEY UPDATE calories_consumed=%s,calorie_goal=%s,updated_at=NOW()',
            (uid,date,calories,goal,calories,goal))

    @classmethod
    def today(cls, uid, date):
        return cls.fetch_one('SELECT * FROM calorie_logs WHERE user_id=%s AND log_date=%s',(uid,date))

    @classmethod
    def range(cls, uid, start, end):
        return cls.fetch_all(
            'SELECT * FROM calorie_logs WHERE user_id=%s AND log_date BETWEEN %s AND %s ORDER BY log_date',
            (uid,start,end))
