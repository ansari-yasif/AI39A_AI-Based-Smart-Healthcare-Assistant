"""app/controllers/dashboard_controller.py — Main dashboard data (safe placeholders)"""
from datetime import datetime
import os
from flask import current_app
from app.controllers.base_controller import BaseController
from app.models.user import UserModel
from app.helpers import today_str, week_range, calculate_bmr, calculate_tdee, calculate_bmi


class DashboardController(BaseController):

    @classmethod
    def _template_exists(cls, template_name):
        path = os.path.join(current_app.root_path, 'templates', template_name)
        return os.path.isfile(path)

    @classmethod
    def index(cls):
        uid = cls.uid()
        today = today_str()
        ws, we = week_range()
        user = UserModel.find_by_id(uid)

        # ---- PLACEHOLDER DATA (replace with real models later) ----
        totals = {'cal': 0, 'prot': 0, 'carbs': 0, 'fat': 0}
        sleep_today = None
        avg_sleep = 0.0
        mood_today = None
        wkt = {'sessions': 0, 'mins': 0, 'burned': 0}
        sleep_labels = []
        sleep_data = []
        cal_labels = []
        cal_chart = []

        # ---- BMR / TDEE / BMI from user profile ----
        bmr = tdee = bmi = 0
        bmi_label = bmi_color = ''
        if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
            weight = float(user['weight_kg'])
            height = float(user['height_cm'])
            age = int(user['age'])
            gender = user.get('gender', 'male')
            bmr = calculate_bmr(weight, height, age, gender)
            tdee = calculate_tdee(bmr, float(user.get('activity_level', 1.55)))
            bmi, bmi_label, bmi_color = calculate_bmi(weight, height)

        calorie_goal = int(tdee) if tdee else 2000

        # ---- Template selection (admin dashboard optional) ----
        template = 'dashboard.html'
        if user and user.get('role') == 'admin':
            admin_template = 'admin_dashboard.html'
            if cls._template_exists(admin_template):
                template = admin_template

        return cls.render(template,
            user=user,
            today=today,
            now=datetime.now(),
            totals=totals,
            calorie_goal=calorie_goal,
            sleep_today=sleep_today,
            avg_sleep=avg_sleep,
            mood_today=mood_today,
            wkt=wkt,
            bmr=bmr,
            tdee=tdee,
            bmi=bmi,
            bmi_label=bmi_label,
            bmi_color=bmi_color,
            sleep_labels=sleep_labels,
            sleep_data=sleep_data,
            cal_labels=cal_labels,
            cal_chart=cal_chart,
        )