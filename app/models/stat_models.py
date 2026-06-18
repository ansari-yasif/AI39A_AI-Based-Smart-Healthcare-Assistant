from app.models.database import db   # <-- your actual db object from app/database.py
from datetime import date, timedelta

def get_contact_info():
    try:
        rows = db.fetch_all("SELECT setting_key, setting_value FROM site_settings")
        contact = {}
        for row in rows:
            contact[row['setting_key']] = row['setting_value']
        return {
            'address': contact.get('contact_address', 'Kathmandu, Putalisadak'),
            'phone': contact.get('contact_phone', '+977 9765682939'),
            'email': contact.get('contact_email', 'vitapulse123@gmail.com')
        }
    except Exception as e:
        print("get_contact_info error:", e)
        return {
            'address': 'Kathmandu, Putalisadak',
            'phone': '+977 9765682939',
            'email': 'vitapulse123@gmail.com'
        }

def get_food_count(user_id):
    result = db.fetch_one("SELECT COUNT(*) as cnt FROM meals WHERE user_id = %s", (user_id,))
    return result['cnt'] if result else 0

def get_meals_count(user_id):
    result = db.fetch_one("SELECT COUNT(*) as cnt FROM meals WHERE user_id = %s", (user_id,))
    return result['cnt'] if result else 0

def get_today_calories(user_id):
    result = db.fetch_one("SELECT SUM(calories) as total FROM meals WHERE user_id = %s AND log_date = CURDATE()", (user_id,))
    return result['total'] if result and result['total'] else 0

def get_calorie_goal(user_id):
    row = db.fetch_one("SELECT calorie_goal FROM calorie_logs WHERE user_id = %s AND log_date = CURDATE()", (user_id,))
    if row and row.get('calorie_goal'):
        return row['calorie_goal']
    row = db.fetch_one("SELECT calorie_goal FROM calorie_logs WHERE user_id = %s ORDER BY log_date DESC LIMIT 1", (user_id,))
    return row['calorie_goal'] if row else 2000

def get_weekly_calories(user_id):
    result = db.fetch_one("""
        SELECT SUM(calories) as total FROM meals 
        WHERE user_id = %s AND log_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
    """, (user_id,))
    return result['total'] if result and result['total'] else 0

def get_workouts_week(user_id):
    result = db.fetch_one("""
        SELECT COUNT(*) as cnt FROM workouts 
        WHERE user_id = %s AND log_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
    """, (user_id,))
    return result['cnt'] if result else 0

def get_avg_sleep_week(user_id):
    result = db.fetch_one("""
        SELECT AVG(hours_slept) as avg_sleep FROM sleep_logs 
        WHERE user_id = %s AND log_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
    """, (user_id,))
    avg = result['avg_sleep'] if result and result['avg_sleep'] else 0
    return round(avg, 1)

def get_today_mood(user_id):
    result = db.fetch_one("SELECT mood FROM mood_logs WHERE user_id = %s AND log_date = CURDATE()", (user_id,))
    return result['mood'] if result else 'Not logged'

def get_user_stats_from_db(user_id):
    if user_id is None:
        return None
    try:
        return {
            "food_items_added": get_food_count(user_id),
            "total_meals": get_meals_count(user_id),
            "calories_today": get_today_calories(user_id),
            "calorie_goal": get_calorie_goal(user_id),
            "weekly_calories": get_weekly_calories(user_id),
            "workouts_this_week": get_workouts_week(user_id),
            "sleep_avg": get_avg_sleep_week(user_id),
            "mood_today": get_today_mood(user_id)
        }
    except Exception as e:
        print("Error fetching user stats:", e)
        return None  # fallback to guest mode