"""app/helpers.py — Pure utility functions for health calculations and validation"""
from datetime import date, datetime, timedelta
from typing import Dict, Tuple


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str = 'male') -> float:
    """Mifflin-St Jeor BMR equation."""
    base = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    return round(base + 5 if gender == 'male' else base - 161, 1)


def calculate_tdee(bmr: float, activity: float) -> float:
    return round(bmr * activity, 1)


def calculate_bmi(weight_kg: float, height_cm: float) -> Tuple[float, str, str]:
    """Return (bmi, label, color) – independent of BMI_RANGES."""
    if height_cm <= 0:
        return 0.0, 'Invalid', '#999'
    h = height_cm / 100
    bmi = round(weight_kg / (h * h), 1)
    if bmi < 18.5:
        return bmi, 'Underweight', '#f97316'
    elif bmi < 25:
        return bmi, 'Normal', '#10b981'
    elif bmi < 30:
        return bmi, 'Overweight', '#f59e0b'
    else:
        return bmi, 'Obese', '#ef4444'


def calculate_macros(tdee: float, goal: str = 'maintain') -> Dict[str, int]:
    splits = {
        'lose':     {'p': 0.35, 'c': 0.35, 'f': 0.30},
        'maintain': {'p': 0.30, 'c': 0.40, 'f': 0.30},
        'gain':     {'p': 0.25, 'c': 0.50, 'f': 0.25},
    }
    s = splits.get(goal, splits['maintain'])
    return {
        'protein': round((tdee * s['p']) / 4),
        'carbs':   round((tdee * s['c']) / 4),
        'fat':     round((tdee * s['f']) / 9),
    }


def today_str() -> str:
    return date.today().isoformat()


def week_range() -> Tuple[str, str]:
    today = date.today()
    start = today - timedelta(days=today.weekday())
    return start.isoformat(), (start + timedelta(days=6)).isoformat()


def month_range() -> Tuple[str, str]:
    today = date.today()
    first = today.replace(day=1)
    if today.month == 12:
        last = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    return first.isoformat(), last.isoformat()


def is_valid_email(email: str) -> bool:
    import re
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))


def is_strong_password(pwd: str) -> bool:
    return (len(pwd) >= 8 and
            any(c.isupper() for c in pwd) and
            any(c.islower() for c in pwd) and
            any(c.isdigit() for c in pwd))


def sanitize(val: str, max_len: int = 255) -> str:
    return val.strip()[:max_len] if val else ''