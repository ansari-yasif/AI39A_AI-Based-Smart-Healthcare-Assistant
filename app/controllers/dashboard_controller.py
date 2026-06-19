"""app/controllers/dashboard_controller.py — Main dashboard with live tracker data"""
from datetime import datetime, date, timedelta
import os
from flask import current_app
from app.controllers.base_controller import BaseController
from app.models.user import UserModel
from app.models.meal import MealModel
from app.models.calorie import CalorieModel
from app.models.sleep import SleepModel
from app.models.mood import MoodModel
from app.models.weight import WeightModel
from app.models.workout import WorkoutModel
from app.helpers import today_str, week_range, calculate_bmr, calculate_tdee, calculate_bmi
from app.models.outbreak import OutbreakModel
from app.models.medicine import MedicineModel
from app.models.expense import ExpenseModel


class DashboardController(BaseController):

    @classmethod
    def _template_exists(cls, name):
        return os.path.isfile(
            os.path.join(current_app.root_path, 'templates', name)
        )

    @classmethod
    def index(cls):
        uid   = cls.uid()
        today = today_str()
        ws, we = week_range()
        user  = UserModel.find_by_id(uid)

        # ── Nutrition ────────────────────────────────────────────────────
        totals = MealModel.totals(uid, today) or {'cal': 0, 'prot': 0, 'carbs': 0, 'fat': 0}

        # 7-day calorie chart
        cal_labels, cal_chart = [], []
        for i in range(6, -1, -1):
            d = (date.today() - timedelta(days=i)).isoformat()
            row = CalorieModel.today(uid, d)
            cal_labels.append(d[5:])
            cal_chart.append(int(row['calories_consumed']) if row else 0)

        # ── Sleep (live) ─────────────────────────────────────────────────
        sleep_today = SleepModel.get_by_date(uid, today)
        sleep_labels, sleep_data = [], []
        for i in range(6, -1, -1):
            d = (date.today() - timedelta(days=i)).isoformat()
            row = SleepModel.get_by_date(uid, d)
            sleep_labels.append(d[5:])
            sleep_data.append(
                round(float(row['hours_slept']), 1) if row and row.get('hours_slept') else 0
            )
        logged_sleep = [h for h in sleep_data if h > 0]
        avg_sleep = round(sum(logged_sleep) / len(logged_sleep), 1) if logged_sleep else 0.0

        # ── Mood (live) ──────────────────────────────────────────────────
        mood_today = MoodModel.get_by_date(uid, today)

        # ── Weight (live) ────────────────────────────────────────────────
        weight_today  = WeightModel.get_by_date(uid, today)
        weight_latest = WeightModel.latest(uid)
        current_weight = round(float(weight_latest['weight_kg']), 1) if weight_latest else 0

        # 14-day weight chart
        weight_labels, weight_chart = [], []
        for row in list(reversed(list(WeightModel.recent(uid, 14) or []))):
            weight_labels.append(str(row['log_date'])[5:])
            weight_chart.append(float(row['weight_kg']))

        # ── Workout (live) ───────────────────────────────────────────────
        start_week = (date.today() - timedelta(days=date.today().weekday())).isoformat()
        wkt = WorkoutModel.week_total(uid, start_week, today)
        recent_workouts = WorkoutModel.recent(uid, 3) or []

        # ── BMR / TDEE / BMI ─────────────────────────────────────────────
        bmr = tdee = bmi = 0
        bmi_label = bmi_color = ''
        if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
            try:
                wkg = float(user['weight_kg'] or 0)
                hcm = float(user['height_cm'] or 0)
                age = int(user['age'] or 0)
                if wkg and hcm and age:
                    bmr = calculate_bmr(wkg, hcm, age, user.get('gender', 'male'))
                    tdee = calculate_tdee(bmr, float(user.get('activity_level') or 1.55))
                    bmi, bmi_label, bmi_color = calculate_bmi(wkg, hcm)
            except Exception:
                pass

        # ── Calorie goal ──────────────────────────────────────────────────
        _saved = CalorieModel.today(uid, today)
        if _saved and _saved.get('calorie_goal'):
            calorie_goal = int(_saved['calorie_goal'])
        elif tdee:
            calorie_goal = int(tdee)
        else:
            calorie_goal = 2000

        template = 'dashboard.html'
        if user and user.get('role') == 'admin' and cls._template_exists('admin_dashboard.html'):
            template = 'admin_dashboard.html'

        return cls.render(template,
            user=user,
            today=today,
            now=datetime.now(),
            # Nutrition
            totals=totals,
            calorie_goal=calorie_goal,
            cal_labels=cal_labels,
            cal_chart=cal_chart,
            macro_today=totals,
            # Sleep
            sleep_today=sleep_today,
            avg_sleep=avg_sleep,
            sleep_labels=sleep_labels,
            sleep_data=sleep_data,
            # Mood
            mood_today=mood_today,
            # Weight
            weight_today=weight_today,
            current_weight=current_weight,
            weight_labels=weight_labels,
            weight_chart=weight_chart,
            # Workout
            wkt=wkt,
            recent_workouts=recent_workouts,
            # Health metrics
            bmr=bmr,
            tdee=tdee,
            bmi=bmi,
            bmi_label=bmi_label,
            bmi_color=bmi_color,
            # Wellness widgets
            outbreak_alerts=OutbreakModel.active_alerts(),
            meds_today=len(MedicineModel.get_for_user(uid)),
            expense_total=cls._month_expense_total(uid),
            workout_daily_target=cls._workout_daily_target(user),
        )

    @classmethod
    def _month_expense_total(cls, uid):
        from app.helpers import month_range
        try:
            ms, me = month_range()
            row = ExpenseModel.total_for_period(uid, ms, me)
            return row.get('total', 0)
        except Exception:
            return 0

    @classmethod
    def _workout_daily_target(cls, user):
        goal = (user.get('goal') if user else None) or 'maintain'
        if goal == 'lose':
            return 400
        elif goal == 'gain':
            return 200
        return 300


    @classmethod
    def notifications_json(cls):
        """JSON API for real-time notification bell."""
        from flask import jsonify
        from datetime import datetime
        uid = cls.uid()
        try:
            from app.models.notification import NotificationModel
            notifs = NotificationModel.get_for_user(uid, 20)
            count = NotificationModel.unread_count(uid)
            def time_ago(dt):
                if not dt: return ''
                now = datetime.now()
                diff = now - dt
                s = diff.total_seconds()
                if s < 60: return 'just now'
                if s < 3600: return f"{int(s//60)}m ago"
                if s < 86400: return f"{int(s//3600)}h ago"
                return f"{int(s//86400)}d ago"
            items = [{
                'id': n['id'],
                'title': n['title'],
                'body': n.get('body',''),
                'type': n.get('type','info'),
                'read': bool(n.get('is_read',0)),
                'link': n.get('link',''),
                'time_ago': time_ago(n['created_at']) if n.get('created_at') else '',
            } for n in (notifs or [])]
            return jsonify({'notifications': items, 'unread': count})
        except Exception as e:
            return jsonify({'notifications': [], 'unread': 0})

    @classmethod
    def notifications_mark_read(cls):
        from flask import request, jsonify
        from app.models.notification import NotificationModel
        uid = cls.uid()
        nid = request.json.get('id') if request.json else None
        if nid:
            NotificationModel.mark_read(nid, uid)
        return jsonify({'ok': True})

    @classmethod
    def notifications_mark_all_read(cls):
        from flask import jsonify
        from app.models.notification import NotificationModel
        uid = cls.uid()
        NotificationModel.mark_all_read(uid)
        return jsonify({'ok': True})
