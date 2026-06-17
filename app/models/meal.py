"""app/models/meal.py — Meal entries | Feature: Meal Tracker"""
from app.models.base_model import BaseModel

class MealModel(BaseModel):
    TABLE = 'meals'

    @classmethod
    def add(cls, uid, name, meal_type, calories, protein, carbs, fat, log_date):
        return cls.execute(
            'INSERT INTO meals(user_id,food_name,meal_type,calories,protein_g,carbs_g,fat_g,log_date,created_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,NOW())',
            (uid,name,meal_type,calories,protein,carbs,fat,log_date))

    @classmethod
    def by_date(cls, uid, date):
        return cls.fetch_all('SELECT * FROM meals WHERE user_id=%s AND log_date=%s ORDER BY created_at',(uid,date))

    @classmethod
    def totals(cls, uid, date):
        row = cls.fetch_one(
            'SELECT COALESCE(SUM(calories),0) AS cal,COALESCE(SUM(protein_g),0) AS prot,COALESCE(SUM(carbs_g),0) AS carbs,COALESCE(SUM(fat_g),0) AS fat FROM meals WHERE user_id=%s AND log_date=%s',
            (uid,date))
        return row or {'cal':0,'prot':0,'carbs':0,'fat':0}

    @classmethod
    def delete(cls, mid, uid):
        return cls.execute('DELETE FROM meals WHERE id=%s AND user_id=%s',(mid,uid))
