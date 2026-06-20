"""app/controllers/nutrition_controller.py — Nutrition feature logic (MVC Controller)"""
from datetime import date
from flask import request, redirect, url_for, flash, jsonify, session
from app.controllers.base_controller import BaseController
from app.models.calorie import CalorieModel
from app.models.meal import MealModel
from app.models.food import FoodModel
from app.models.user import UserModel
from app.helpers import today_str, calculate_bmr, calculate_tdee, calculate_bmi, calculate_macros
from app.models.bmi import BMIModel
from app.models.notification import NotificationModel
from app.models.macro_target import MacroTargetModel


class NutritionController(BaseController):

    # ──────────────────────────────────────────────────────────────────────
    # CALORIE CALCULATOR PAGE  (GET /nutrition/calories)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def calorie_index(cls):
        uid   = cls.uid()
        today = today_str()
        user  = UserModel.find_by_id(uid)

        bmr = tdee = bmi = 0
        bmi_label = bmi_color = ''
        macros = {}
        calorie_log = None

        if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
            w  = float(user['weight_kg'])
            h  = float(user['height_cm'])
            a  = int(user['age'])
            g  = user.get('gender', 'male')
            al = float(user.get('activity_level', 1.55))
            goal = user.get('goal', 'maintain')

            bmr  = calculate_bmr(w, h, a, g)
            tdee = calculate_tdee(bmr, al)
            bmi, bmi_label, bmi_color = calculate_bmi(w, h)
            macros = calculate_macros(tdee, goal)

        calorie_log  = CalorieModel.today(uid, today)

        # Respect user's manually-set goal from DB; only fall back to TDEE
        # when there is NO saved record at all (first visit).
        if calorie_log and calorie_log.get('calorie_goal'):
            calorie_goal = int(calorie_log['calorie_goal'])
        elif tdee:
            calorie_goal = int(tdee)
            # First time — seed the record so there's something in the DB
            CalorieModel.log(uid, today,
                             calorie_log['calories_consumed'] if calorie_log else 0,
                             calorie_goal)
            calorie_log = CalorieModel.today(uid, today)
        else:
            calorie_goal = 2000

        meals_today = MealModel.by_date(uid, today)
        totals      = MealModel.totals(uid, today)

        # 7-day calorie history for chart
        from datetime import timedelta
        labels, chart_data, goal_line = [], [], []
        for i in range(6, -1, -1):
            d = (date.today() - timedelta(days=i)).isoformat()
            row = CalorieModel.today(uid, d)
            labels.append(d[5:])        # MM-DD
            chart_data.append(int(row['calories_consumed']) if row else 0)
            goal_line.append(calorie_goal)

        return cls.render('nutrition/calorie_calculator.html',
            user=user, today=today,
            bmr=bmr, tdee=tdee, bmi=bmi,
            bmi_label=bmi_label, bmi_color=bmi_color,
            macros=macros,
            calorie_goal=calorie_goal,
            calorie_log=calorie_log,
            meals_today=meals_today,
            totals=totals,
            cal_labels=labels,
            cal_chart=chart_data,
            cal_goal_line=goal_line,
        )

    # ──────────────────────────────────────────────────────────────────────
    # UPDATE CALORIE GOAL  (POST /nutrition/calories/goal)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def update_goal(cls):
        uid   = cls.uid()
        today = today_str()
        goal  = int(request.form.get('calorie_goal', 2000))
        existing = CalorieModel.today(uid, today)
        consumed  = int(existing['calories_consumed']) if existing else 0
        CalorieModel.log(uid, today, consumed, goal)
        flash('Daily calorie goal updated!', 'success')
        return redirect(url_for('nutrition.calorie_index'))

    # ──────────────────────────────────────────────────────────────────────
    # MEAL TRACKER PAGE  (GET /nutrition/meals)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def meal_index(cls):
        uid   = cls.uid()
        today = today_str()
        date_param = request.args.get('date', today)

        meals  = MealModel.by_date(uid, date_param)
        totals = MealModel.totals(uid, date_param)

        cal_log      = CalorieModel.today(uid, today)
        user         = UserModel.find_by_id(uid)
        calorie_goal = 2000
        if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
            bmr = calculate_bmr(float(user['weight_kg']), float(user['height_cm']),
                                int(user['age']), user.get('gender', 'male'))
            calorie_goal = int(calculate_tdee(bmr, float(user.get('activity_level', 1.55))))

        # Group meals by type
        grouped = {'Breakfast': [], 'Lunch': [], 'Dinner': [], 'Snack': []}
        for m in meals:
            t = m.get('meal_type', 'Snack')
            grouped.setdefault(t, []).append(m)

        return cls.render('nutrition/meal_tracker.html',
            meals=meals,
            grouped=grouped,
            totals=totals,
            calorie_goal=calorie_goal,
            selected_date=date_param,
            today=today,
        )

    # ──────────────────────────────────────────────────────────────────────
    # LOG A MEAL  (POST /nutrition/meals/add)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def add_meal(cls):
        uid  = cls.uid()
        f    = request.form
        name      = f.get('food_name', '').strip()
        meal_type = f.get('meal_type', 'Snack')
        calories  = float(f.get('calories', 0))
        protein   = float(f.get('protein', 0))
        carbs     = float(f.get('carbs', 0))
        fat       = float(f.get('fat', 0))
        log_date  = f.get('log_date', today_str())

        if not name:
            flash('Food name is required.', 'danger')
            return redirect(url_for('nutrition.meal_index'))

        MealModel.add(uid, name, meal_type, calories, protein, carbs, fat, log_date)

        # Update calorie log totals — preserve user's saved goal
        totals = MealModel.totals(uid, log_date)
        saved  = CalorieModel.today(uid, log_date)
        if saved and saved.get('calorie_goal'):
            calorie_goal = int(saved['calorie_goal'])
        else:
            user = UserModel.find_by_id(uid)
            calorie_goal = 2000
            if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
                wkg = float(user.get('weight_kg') or 0)
                hcm = float(user.get('height_cm') or 0)
                age = int(user.get('age') or 0)
                if wkg and hcm and age:
                    bmr = calculate_bmr(wkg, hcm, age, user.get('gender', 'male'))
                    calorie_goal = int(calculate_tdee(bmr, float(user.get('activity_level') or 1.55)))
        CalorieModel.log(uid, log_date, int(totals.get('cal', 0) or 0), calorie_goal)

        flash(f'"{name}" added to your meal log!', 'success')
        return redirect(url_for('nutrition.meal_index', date=log_date))

    # ──────────────────────────────────────────────────────────────────────
    # DELETE A MEAL  (POST /nutrition/meals/delete/<id>)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def delete_meal(cls, meal_id):
        uid      = cls.uid()
        today    = today_str()
        MealModel.delete(meal_id, uid)
        totals = MealModel.totals(uid, today)
        saved  = CalorieModel.today(uid, today)
        if saved and saved.get('calorie_goal'):
            calorie_goal = int(saved['calorie_goal'])
        else:
            user = UserModel.find_by_id(uid)
            calorie_goal = 2000
            if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
                wkg = float(user.get('weight_kg') or 0)
                hcm = float(user.get('height_cm') or 0)
                age = int(user.get('age') or 0)
                if wkg and hcm and age:
                    bmr = calculate_bmr(wkg, hcm, age, user.get('gender', 'male'))
                    calorie_goal = int(calculate_tdee(bmr, float(user.get('activity_level') or 1.55)))
        CalorieModel.log(uid, today, int(totals.get('cal', 0) or 0), calorie_goal)
        flash('Meal removed.', 'info')
        return redirect(url_for('nutrition.meal_index'))

    # ──────────────────────────────────────────────────────────────────────
    # FOOD DATABASE PAGE  (GET /nutrition/foods)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def food_db_index(cls):
        uid      = cls.uid()
        query    = request.args.get('q', '').strip()
        category = request.args.get('category', '')

        if query:
            results = FoodModel.search(query)
        elif category:
            results = FoodModel.by_category(category)
        else:
            results = FoodModel.FOOD_DB[:30]

        categories   = FoodModel.categories()
        custom_foods = FoodModel.get_custom_by_user(uid)

        # Normalize custom foods — use offset ID to avoid collision with static food IDs
        from app.models.food import FoodModel as _FM
        custom_normalized = []
        for cf in custom_foods:
            custom_normalized.append({
                'id':       cf['id'] + _FM.CUSTOM_ID_OFFSET,
                'name':     cf['name'],
                'category': cf.get('category', 'Custom'),
                'calories': cf['calories'],
                'protein':  cf.get('protein_g', cf.get('protein', 0)),
                'carbs':    cf.get('carbs_g', cf.get('carbs', 0)),
                'fat':      cf.get('fat_g', cf.get('fat', 0)),
            })

        today        = today_str()

        return cls.render('nutrition/food_database.html',
            results=results,
            query=query,
            category=category,
            categories=categories,
            custom_foods=custom_foods,
            custom_normalized=custom_normalized,
            today=today,
        )

    # ──────────────────────────────────────────────────────────────────────
    # FOOD SEARCH API  (GET /nutrition/foods/search?q=...) — JSON
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def food_search_api(cls):
        q       = request.args.get('q', '').strip()
        results = FoodModel.search(q, limit=15)
        return jsonify(results)

    # ──────────────────────────────────────────────────────────────────────
    # ADD CUSTOM FOOD  (POST /nutrition/foods/custom/add)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def add_custom_food(cls):
        uid  = cls.uid()
        f    = request.form
        name     = f.get('name', '').strip()
        calories = float(f.get('calories', 0))
        protein  = float(f.get('protein', 0))
        carbs    = float(f.get('carbs', 0))
        fat      = float(f.get('fat', 0))

        if not name:
            flash('Food name is required.', 'danger')
            return redirect(url_for('nutrition.food_db_index') + '#custom')

        FoodModel.add_custom(uid, name, calories, protein, carbs, fat)
        flash(f'Custom food "{name}" added!', 'success')
        return redirect(url_for('nutrition.food_db_index') + '#custom')

    # ──────────────────────────────────────────────────────────────────────
    # DELETE CUSTOM FOOD  (POST /nutrition/foods/custom/delete/<id>)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def delete_custom_food(cls, cid):
        uid = cls.uid()
        FoodModel.delete_custom(cid, uid)
        flash('Custom food deleted.', 'info')
        return redirect(url_for('nutrition.food_db_index') + '#custom')

    # ──────────────────────────────────────────────────────────────────────
    # QUICK ADD FROM FOOD DB → MEAL LOG  (POST /nutrition/foods/quick-add)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def quick_add_to_meal(cls):
        uid      = cls.uid()
        f        = request.form
        food_id  = int(f.get('food_id', 0))
        meal_type = f.get('meal_type', 'Snack')
        log_date  = f.get('log_date', today_str())

        food = FoodModel.get_by_id(food_id)
        if not food:
            flash('Food not found.', 'danger')
            return redirect(url_for('nutrition.food_db_index'))

        MealModel.add(uid, food['name'], meal_type,
                      food['calories'], food['protein'],
                      food['carbs'], food['fat'], log_date)

        # Update calorie log — preserve user's saved goal
        totals = MealModel.totals(uid, log_date)
        saved  = CalorieModel.today(uid, log_date)
        if saved and saved.get('calorie_goal'):
            calorie_goal = int(saved['calorie_goal'])
        else:
            user = UserModel.find_by_id(uid)
            calorie_goal = 2000
            if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
                wkg = float(user.get('weight_kg') or 0)
                hcm = float(user.get('height_cm') or 0)
                age = int(user.get('age') or 0)
                if wkg and hcm and age:
                    bmr = calculate_bmr(wkg, hcm, age, user.get('gender', 'male'))
                    calorie_goal = int(calculate_tdee(bmr, float(user.get('activity_level') or 1.55)))
        CalorieModel.log(uid, log_date, int(totals.get('cal', 0) or 0), calorie_goal)

        flash(f'"{food["name"]}" added to your {meal_type}!', 'success')
        return redirect(url_for('nutrition.meal_index', date=log_date))

    # ──────────────────────────────────────────────────────────────────────
    # BMI CALCULATOR PAGE  (GET /nutrition/bmi)
    # ──────────────────────────────────────────────────────────────────────
    # BMI CALCULATOR — DB-backed (persistent across sessions)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def bmi_index(cls):
        uid  = cls.uid()
        user = UserModel.find_by_id(uid)
        bmi = bmi_label = bmi_color = ''
        prefill_weight = prefill_height = ''

        # Try latest DB record for pre-fill
        latest = BMIModel.latest(uid)
        if latest:
            prefill_weight = latest['weight_kg']
            prefill_height = latest['height_cm']
            bmi, bmi_label, bmi_color = latest['bmi_value'], latest['bmi_label'], latest['bmi_color']
        elif user:
            prefill_weight = user.get('weight_kg', '')
            prefill_height = user.get('height_cm', '')
            if prefill_weight and prefill_height:
                bmi, bmi_label, bmi_color = calculate_bmi(float(prefill_weight), float(prefill_height))

        bmi_history = BMIModel.history(uid, limit=10)
        return cls.render('nutrition/bmi_calculator.html',
            user=user,
            bmi=bmi, bmi_label=bmi_label, bmi_color=bmi_color,
            prefill_weight=prefill_weight, prefill_height=prefill_height,
            bmi_history=bmi_history,
            today=today_str(),
        )

    @classmethod
    def bmi_calculate(cls):
        try:
            weight = float(request.form.get('weight', 0))
            height = float(request.form.get('height', 0))
        except (ValueError, TypeError):
            weight = height = 0
        if not weight or not height:
            flash('Please enter valid weight and height.', 'danger')
            return redirect(url_for('nutrition.bmi_index'))
        bmi_val, bmi_label, bmi_color = calculate_bmi(weight, height)
        uid = cls.uid()
        # Save to database — persists across logout/login
        BMIModel.save(uid, weight, height, bmi_val, bmi_label, bmi_color)
        # Generate a notification for interesting BMI changes
        latest_two = BMIModel.history(uid, limit=2)
        if len(latest_two) >= 2:
            prev = float(latest_two[1]['bmi_value'])
            diff = round(bmi_val - prev, 1)
            if abs(diff) >= 0.5:
                direction = 'increased' if diff > 0 else 'decreased'
                NotificationModel.create(uid,
                    f'BMI {direction} by {abs(diff)} points',
                    f'Your BMI changed from {prev} to {bmi_val} ({bmi_label}).',
                    'health', '/nutrition/bmi')
        user = UserModel.find_by_id(uid)
        bmi_history = BMIModel.history(uid, limit=10)
        return cls.render('nutrition/bmi_calculator.html',
            user=user,
            bmi=bmi_val, bmi_label=bmi_label, bmi_color=bmi_color,
            prefill_weight=weight, prefill_height=height,
            bmi_history=bmi_history,
            today=today_str(),
        )

    # ──────────────────────────────────────────────────────────────────────
    # REPORTS PAGE  (GET /nutrition/reports)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def _build_report_data(cls, uid, days=7):
        from datetime import timedelta
        today = date.today()
        labels = []
        cal_data, prot_data, carbs_data, fat_data = [], [], [], []
        sleep_data, mood_data, weight_data = [], [], []

        # Lazy-import models to avoid circular imports
        try:
            from app.models.sleep import SleepModel
            has_sleep = True
        except ImportError:
            has_sleep = False
        try:
            from app.models.mood import MoodModel
            has_mood = True
        except ImportError:
            has_mood = False
        try:
            from app.models.weight import WeightModel
            has_weight = True
        except ImportError:
            has_weight = False

        for i in range(days - 1, -1, -1):
            d = (today - timedelta(days=i)).isoformat()
            row    = CalorieModel.today(uid, d)
            totals = MealModel.totals(uid, d)
            labels.append(d[5:])
            cal_data.append(int(row['calories_consumed']) if row else 0)
            prot_data.append(round(float(totals.get('prot') or 0), 1))
            carbs_data.append(round(float(totals.get('carbs') or 0), 1))
            fat_data.append(round(float(totals.get('fat') or 0), 1))

            if has_sleep:
                try:
                    sr = SleepModel.get_by_date(uid, d)
                    sleep_data.append(round(float(sr['hours_slept']) if sr and sr.get('hours_slept') else 0, 1))
                except Exception:
                    sleep_data.append(0)
            else:
                sleep_data.append(0)

            if has_mood:
                try:
                    mr = MoodModel.get_by_date(uid, d)
                    mood_data.append(int(mr['energy_level']) if mr and mr.get('energy_level') else 0)
                except Exception:
                    mood_data.append(0)
            else:
                mood_data.append(0)

            if has_weight:
                try:
                    wr = WeightModel.get_by_date(uid, d)
                    weight_data.append(float(wr['weight_kg']) if wr and wr.get('weight_kg') else 0)
                except Exception:
                    weight_data.append(0)
            else:
                weight_data.append(0)

        logged_days = sum(1 for x in cal_data if x > 0) or 1
        avg_cal   = round(sum(cal_data) / logged_days, 1)
        total_cal = sum(cal_data)
        avg_prot  = round(sum(prot_data) / logged_days, 1)
        avg_carbs = round(sum(carbs_data) / logged_days, 1)
        avg_fat   = round(sum(fat_data) / logged_days, 1)
        max_cal   = max(cal_data) if cal_data else 0
        min_cal   = min([c for c in cal_data if c > 0] or [0])
        days_logged = len([c for c in cal_data if c > 0])

        slept_days = sum(1 for x in sleep_data if x > 0) or 1
        avg_sleep = round(sum(sleep_data) / slept_days, 1)
        avg_mood  = round(sum([m for m in mood_data if m > 0]) / max(len([m for m in mood_data if m > 0]), 1), 1)

        # Latest weight from BMI records
        latest_bmi = BMIModel.latest(uid)
        current_weight = float(latest_bmi['weight_kg']) if latest_bmi else 0
        current_bmi    = float(latest_bmi['bmi_value']) if latest_bmi else 0
        bmi_label_str  = latest_bmi['bmi_label'] if latest_bmi else '—'

        return {
            'labels': labels, 'cal_data': cal_data,
            'prot_data': prot_data, 'carbs_data': carbs_data, 'fat_data': fat_data,
            'sleep_data': sleep_data, 'mood_data': mood_data, 'weight_data': weight_data,
            'avg_cal': avg_cal, 'total_cal': total_cal, 'days_logged': days_logged,
            'avg_prot': avg_prot, 'avg_carbs': avg_carbs, 'avg_fat': avg_fat,
            'max_cal': max_cal, 'min_cal': min_cal,
            'avg_sleep': avg_sleep, 'avg_mood': avg_mood,
            'current_weight': current_weight, 'current_bmi': current_bmi,
            'bmi_label': bmi_label_str,
            'days': days,
        }

    @classmethod
    def reports_index(cls):
        uid = cls.uid()
        user = UserModel.find_by_id(uid)
        weekly  = cls._build_report_data(uid, 7)
        monthly = cls._build_report_data(uid, 30)
        calorie_goal = 2000
        if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
            bmr = calculate_bmr(float(user['weight_kg']), float(user['height_cm']),
                                int(user['age']), user.get('gender', 'male'))
            calorie_goal = int(calculate_tdee(bmr, float(user.get('activity_level', 1.55))))
        recs = cls._build_recommendations(uid, user, weekly)
        return cls.render('nutrition/reports.html',
            user=user,
            weekly=weekly, monthly=monthly,
            calorie_goal=calorie_goal,
            recs=recs,
            today=today_str(),
        )

    @classmethod
    def _empty_report(cls, days, error=''):
        """Safe empty report for when DB tables don't exist yet."""
        from app.helpers import today_str
        from datetime import date, timedelta
        labels = [(date.today() - timedelta(days=i)).strftime('%m-%d') for i in range(days-1,-1,-1)]
        return {
            'days': days, 'days_logged': 0, 'error': error,
            'labels': labels,
            'cal_data': [0]*days, 'prot_data': [0]*days,
            'carbs_data': [0]*days, 'fat_data': [0]*days, 'sleep_data': [0]*days,
            'total_cal': 0, 'avg_cal': 0, 'max_cal': 0,
            'avg_prot': 0, 'avg_carbs': 0, 'avg_fat': 0,
            'avg_sleep': 0, 'current_bmi': 0,
            'bmi_label': 'N/A', 'bmi_color': '#94a3b8',
            'mood_freq': {}, 'weight_trend': [],
        }

    @classmethod
    def _generate_pdf(cls, report_type, days):
        """Comprehensive PDF with all health data."""
        from flask import make_response
        import io
        uid  = cls.uid()
        user = UserModel.find_by_id(uid)
        data = cls._build_report_data(uid, days)
        username = (user.get('full_name') or 'User') if user else 'User'

        # Personalised recommendations text
        recs = cls._build_recommendations(uid, user, data)

        # Wellness data (medicine adherence, expenses, health risk)
        from app.models.medicine import MedicineModel
        from app.models.expense import ExpenseModel
        from app.controllers.wellness_controller import WellnessController
        from app.helpers import month_range

        adherence_pct = MedicineModel.adherence_rate(uid, days)
        active_meds = MedicineModel.get_for_user(uid)

        ms, me = month_range()
        expense_total = ExpenseModel.total_for_period(uid, ms, me)
        expense_by_cat = ExpenseModel.by_category(uid, ms, me)

        avg_cal_7d = WellnessController._avg_calories_7d(uid)
        health_risks = WellnessController._compute_risks(user, data['current_bmi'], avg_cal_7d)

        workout_plan_data = WellnessController._build_workout_plan_data(uid, user)

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors as rl_colors
            from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                             Table, TableStyle, HRFlowable)
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                                    leftMargin=2*cm, rightMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)
            styles = getSampleStyleSheet()

            TEAL       = rl_colors.HexColor('#007C5A')
            BLUE       = rl_colors.HexColor('#1a4fa0')
            DARK_BG    = rl_colors.HexColor('#1a2c3d')
            DARK_BG2   = rl_colors.HexColor('#f0f4f8')
            HEADER_BG  = rl_colors.HexColor('#0a3d2e')
            MUTED      = rl_colors.HexColor('#64748b')
            BLACK      = rl_colors.HexColor('#1e293b')
            LIGHT_GREY = rl_colors.HexColor('#f8fafc')
            GRID_COL   = rl_colors.HexColor('#cbd5e1')
            PAGE_BG    = rl_colors.white

            title_s = ParagraphStyle('T', parent=styles['Normal'],
                fontSize=22, textColor=TEAL, fontName='Helvetica-Bold',
                spaceAfter=4, leading=26)
            sub_s   = ParagraphStyle('S', parent=styles['Normal'],
                fontSize=10, textColor=MUTED, spaceAfter=6)
            h2_s    = ParagraphStyle('H2', parent=styles['Normal'],
                fontSize=13, textColor=BLUE, fontName='Helvetica-Bold',
                spaceBefore=14, spaceAfter=6, leading=16)
            h3_s    = ParagraphStyle('H3', parent=styles['Normal'],
                fontSize=11, textColor=TEAL, fontName='Helvetica-Bold',
                spaceBefore=8, spaceAfter=4, leading=14)
            body_s  = ParagraphStyle('B', parent=styles['Normal'],
                fontSize=9, textColor=BLACK, leading=14, spaceAfter=4)
            rec_s   = ParagraphStyle('R', parent=styles['Normal'],
                fontSize=9, textColor=BLACK, leading=14, leftIndent=10, spaceAfter=3)

            def tbl(data_rows, col_widths, header=True):
                t = Table(data_rows, colWidths=col_widths, repeatRows=1)
                style_cmds = [
                    ('BACKGROUND',    (0,0), (-1,-1), PAGE_BG),
                    ('TEXTCOLOR',     (0,0), (-1,-1), BLACK),
                    ('GRID',          (0,0), (-1,-1), 0.5, GRID_COL),
                    ('FONTSIZE',      (0,0), (-1,-1), 9),
                    ('TOPPADDING',    (0,0), (-1,-1), 5),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                    ('LEFTPADDING',   (0,0), (-1,-1), 6),
                    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
                    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
                    ('WORDWRAP',      (0,0), (-1,-1), 'CJK'),
                ]
                if header:
                    style_cmds += [
                        ('BACKGROUND', (0,0), (-1,0), DARK_BG),
                        ('TEXTCOLOR',  (0,0), (-1,0), rl_colors.white),
                        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',   (0,0), (-1,0), 10),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [PAGE_BG, LIGHT_GREY]),
                    ]
                t.setStyle(TableStyle(style_cmds))
                return t

            story = []

            # ── Cover ──
            story.append(Paragraph(f'VitaPulse — {report_type} Health Report', title_s))
            story.append(Paragraph(
                f'User: {username}  |  Period: Last {days} days  |  Generated: {today_str()}', sub_s))
            story.append(HRFlowable(width='100%', thickness=1, color=TEAL, spaceAfter=10))

            # ── Summary Stats ──
            story.append(Paragraph('Summary Statistics', h2_s))
            stats_rows = [
                ['Metric', 'Value', 'Metric', 'Value'],
                ['Total Calories', f"{data['total_cal']} kcal",
                 'Days Tracked', f"{data['days_logged']}/{days}"],
                ['Avg Daily Calories', f"{data['avg_cal']} kcal",
                 'Peak Day', f"{data['max_cal']} kcal"],
                ['Avg Protein/day', f"{data['avg_prot']}g",
                 'Avg Carbs/day', f"{data['avg_carbs']}g"],
                ['Avg Fat/day', f"{data['avg_fat']}g",
                 'Lowest Logged Day', f"{data['min_cal']} kcal"],
                ['Avg Sleep', f"{data['avg_sleep']}h",
                 'Current BMI', f"{data['current_bmi']} ({data['bmi_label']})"],
            ]
            story.append(tbl(stats_rows, [4.5*cm, 4*cm, 4.5*cm, 4*cm]))
            story.append(Spacer(1, 0.4*cm))

            # ── Nutrition Breakdown ──
            story.append(Paragraph('Daily Nutrition Breakdown', h2_s))
            n_cols = ['Date', 'Calories', 'Protein', 'Carbs', 'Fat']
            n_rows = [n_cols]
            for i, label in enumerate(data['labels']):
                n_rows.append([
                    label,
                    f"{data['cal_data'][i]} kcal",
                    f"{data['prot_data'][i]}g",
                    f"{data['carbs_data'][i]}g",
                    f"{data['fat_data'][i]}g",
                ])
            story.append(tbl(n_rows, [3*cm, 3.5*cm, 3*cm, 3*cm, 2.5*cm]))
            story.append(Spacer(1, 0.4*cm))

            # ── Sleep & Mood ──
            has_sleep_data = any(s > 0 for s in data['sleep_data'])
            has_mood_data  = any(m > 0 for m in data['mood_data'])
            if has_sleep_data or has_mood_data:
                story.append(Paragraph('Sleep and Mood Log', h2_s))
                sm_cols = ['Date', 'Sleep (hrs)', 'Mood Score']
                sm_rows = [sm_cols]
                for i, label in enumerate(data['labels']):
                    sm_rows.append([
                        label,
                        str(data['sleep_data'][i]) if data['sleep_data'][i] > 0 else '—',
                        str(data['mood_data'][i])  if data['mood_data'][i] > 0 else '—',
                    ])
                story.append(tbl(sm_rows, [4*cm, 5*cm, 5*cm]))
                story.append(Spacer(1, 0.4*cm))

            # ── BMI History ──
            bmi_hist = BMIModel.history(uid, limit=days)
            if bmi_hist:
                story.append(Paragraph('BMI History', h2_s))
                bmi_cols = ['Date', 'Weight (kg)', 'Height (cm)', 'BMI', 'Category']
                bmi_rows = [bmi_cols]
                for b in bmi_hist:
                    bmi_rows.append([
                        str(b['recorded_at']),
                        str(b['weight_kg']),
                        str(b['height_cm']),
                        str(b['bmi_value']),
                        b['bmi_label'],
                    ])
                story.append(tbl(bmi_rows, [3.5*cm, 3*cm, 3*cm, 2.5*cm, 3*cm]))
                story.append(Spacer(1, 0.4*cm))

            # ── Health Risk Assessment ──
            story.append(Paragraph('Health Risk Assessment', h2_s))
            story.append(Paragraph(
                f"Overall Risk Level: <b>{health_risks['overall']['level']}</b> "
                f"({health_risks['overall']['pct']}% composite score)", body_s))
            risk_rows = [['Risk Factor', 'Level', 'Details']]
            for r in health_risks.get('items', health_risks.get('risk_list', [])):
                risk_rows.append([r['name'], r['level'], r['desc'][:90]])
            story.append(tbl(risk_rows, [3.5*cm, 2.5*cm, 8*cm]))
            story.append(Paragraph(
                'Note: This is a rule-based estimate, not a medical diagnosis. Consult a healthcare professional.',
                ParagraphStyle('note', parent=styles['Normal'], fontSize=7, textColor=MUTED, spaceAfter=4)))
            story.append(Spacer(1, 0.4*cm))

            # ── Workout Plan Summary ──
            story.append(Paragraph('Workout Plan Summary', h2_s))
            story.append(Paragraph(
                f"Goal: <b>{workout_plan_data['goal'].capitalize()}</b> · "
                f"Daily burn target: <b>{workout_plan_data['daily_target']} kcal</b> · "
                f"Full plan burn potential: <b>{workout_plan_data['daily_burn_total']} kcal</b>", body_s))
            wp_rows = [['Body Part', 'Exercises', 'Est. kcal Burn']]
            for key, part in workout_plan_data['body_parts'].items():
                wp_rows.append([part['name'], str(len(part['exercises'])), f"~{part['total_kcal']} kcal"])
            wp_rows.append(['Cardio Options', str(len(workout_plan_data['cardio'])), f"~{workout_plan_data['cardio_total']} kcal"])
            story.append(tbl(wp_rows, [5*cm, 4*cm, 5*cm]))
            story.append(Spacer(1, 0.4*cm))

            # ── Medicine Adherence ──
            if active_meds:
                story.append(Paragraph('Medicine Adherence', h2_s))
                story.append(Paragraph(
                    f"Adherence rate (last {days} days): <b>{adherence_pct}%</b>", body_s))
                med_rows = [['Medicine', 'Dosage', 'Times', 'Frequency']]
                for m in active_meds:
                    med_rows.append([m['name'], m.get('dosage') or '—', m['times'], m['frequency']])
                story.append(tbl(med_rows, [4*cm, 3*cm, 4.5*cm, 2.5*cm]))
                story.append(Spacer(1, 0.4*cm))

            # ── Health Expense Summary ──
            if expense_by_cat:
                story.append(Paragraph('Health Expense Summary (This Month)', h2_s))
                story.append(Paragraph(
                    f"Total spent this month: <b>{expense_total['total']}</b> across {expense_total['cnt']} transaction(s)", body_s))
                exp_rows = [['Category', 'Total', 'Transactions']]
                for ec in expense_by_cat:
                    exp_rows.append([ec['category'], str(ec['total']), str(ec['cnt'])])
                story.append(tbl(exp_rows, [5*cm, 4*cm, 4*cm]))
                story.append(Spacer(1, 0.4*cm))

            # ── Personalised Recommendations ──
            story.append(Paragraph('Personalised Recommendations', h2_s))
            story.append(Paragraph('Based on your logged health data:', body_s))

            if recs.get('nutrition'):
                story.append(Paragraph('Nutrition', h3_s))
                for r in recs['nutrition']:
                    story.append(Paragraph(f'• {r}', rec_s))
            if recs.get('sleep'):
                story.append(Paragraph('Sleep', h3_s))
                for r in recs['sleep']:
                    story.append(Paragraph(f'• {r}', rec_s))
            if recs.get('workout'):
                story.append(Paragraph('Workout', h3_s))
                for r in recs['workout']:
                    story.append(Paragraph(f'• {r}', rec_s))
            if recs.get('weight'):
                story.append(Paragraph('Weight and BMI', h3_s))
                for r in recs['weight']:
                    story.append(Paragraph(f'• {r}', rec_s))

            story.append(Spacer(1, 0.5*cm))
            story.append(HRFlowable(width='100%', thickness=0.5, color=MUTED))
            story.append(Paragraph(
                'Generated by VitaPulse | Data is for informational purposes only.',
                ParagraphStyle('foot', parent=styles['Normal'],
                               fontSize=7, textColor=MUTED, alignment=1, spaceBefore=6)))

            doc.build(story)
            pdf_bytes = buf.getvalue()
            resp = make_response(pdf_bytes)
            resp.headers['Content-Type'] = 'application/pdf'
            resp.headers['Content-Disposition'] = (
                f'attachment; filename="vitapulse_{report_type.lower()}_report.pdf"')
            return resp

        except ImportError:
            lines = [f'VitaPulse {report_type} Report', f'User: {username}',
                     f'Period: Last {days} days', f'Generated: {today_str()}', '']
            lines.append('Date,Calories,Protein,Carbs,Fat,Sleep,Mood')
            for i, label in enumerate(data['labels']):
                lines.append(','.join([
                    label, str(data['cal_data'][i]),
                    str(data['prot_data'][i]), str(data['carbs_data'][i]),
                    str(data['fat_data'][i]),
                    str(data['sleep_data'][i]), str(data['mood_data'][i]),
                ]))
            resp = make_response('\n'.join(lines))
            resp.headers['Content-Type'] = 'text/csv'
            resp.headers['Content-Disposition'] = (
                f'attachment; filename="vitapulse_{report_type.lower()}_report.csv"')
            return resp
    @classmethod
    def weekly_report_pdf(cls):
        return cls._generate_pdf('Weekly', 7)

    @classmethod
    def monthly_report_pdf(cls):
        return cls._generate_pdf('Monthly', 30)

    # ──────────────────────────────────────────────────────────────────────
    # PERSONALISED RECOMMENDATIONS ENGINE
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def _build_recommendations(cls, uid, user, data=None):
        """Generate data-driven recommendations from logged health data."""
        if data is None:
            data = cls._build_report_data(uid, 7)

        recs = {'nutrition': [], 'sleep': [], 'workout': [], 'weight': []}
        avg_cal   = data.get('avg_cal', 0)
        avg_prot  = data.get('avg_prot', 0)
        avg_carbs = data.get('avg_carbs', 0)
        avg_fat   = data.get('avg_fat', 0)
        avg_sleep = data.get('avg_sleep', 0)
        cur_bmi   = data.get('current_bmi', 0)
        days_logged = data.get('days_logged', 0)
        days      = data.get('days', 7)

        calorie_goal = 2000
        if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
            try:
                wkg = float(user.get('weight_kg') or 0)
                hcm = float(user.get('height_cm') or 0)
                age = int(user.get('age') or 0)
                if wkg and hcm and age:
                    bmr = calculate_bmr(wkg, hcm, age, user.get('gender', 'male'))
                    calorie_goal = int(calculate_tdee(bmr, float(user.get('activity_level') or 1.55)))
            except Exception:
                pass

        # Calorie recommendations
        if avg_cal > 0:
            deficit = calorie_goal - avg_cal
            if deficit > 300:
                recs['nutrition'].append(
                    f'You averaged {int(avg_cal)} kcal/day — {int(deficit)} kcal below your goal of {calorie_goal}. '
                    'Try adding a nutritious snack like nuts or a banana between meals.')
            elif deficit < -300:
                recs['nutrition'].append(
                    f'You averaged {int(avg_cal)} kcal/day — {abs(int(deficit))} kcal above your goal. '
                    'Consider reducing portion sizes or swapping high-calorie snacks for vegetables.')
            else:
                recs['nutrition'].append(
                    f'Great work — you stayed within range of your {calorie_goal} kcal goal averaging {int(avg_cal)} kcal/day.')
        else:
            recs['nutrition'].append('Start logging your meals to get personalised calorie recommendations.')

        # Protein recommendations
        ideal_protein = round(float(user.get('weight_kg') or 70) * 1.6, 1) if user else 112.0
        if avg_prot > 0:
            if avg_prot < ideal_protein * 0.75:
                recs['nutrition'].append(
                    f'Your protein intake averaged {avg_prot}g/day — aim for {ideal_protein}g '
                    '(~1.6g per kg body weight). Add eggs, chicken, lentils, or Greek yogurt.')
            elif avg_prot >= ideal_protein:
                recs['nutrition'].append(
                    f'Excellent protein intake at {avg_prot}g/day — supporting muscle maintenance and satiety.')

        # Carb/fat balance
        if avg_carbs > 0 and avg_fat > 0:
            if avg_fat > avg_cal * 0.40 / 9:
                recs['nutrition'].append(
                    f'Fat contributes a high share of your calories ({avg_fat}g). '
                    'Consider replacing some saturated fats with whole grains, legumes, or fruits.')
            if avg_carbs > avg_cal * 0.65 / 4:
                recs['nutrition'].append(
                    'Carbohydrates are high — prioritise complex carbs like oats, brown rice, '
                    'and vegetables over refined options.')

        # Logging consistency
        if days_logged < days * 0.5:
            recs['nutrition'].append(
                f'You logged only {days_logged}/{days} days. '
                'Consistent logging is the #1 predictor of reaching nutrition goals.')

        # Sleep recommendations
        if avg_sleep > 0:
            if avg_sleep < 6:
                recs['sleep'].append(
                    f'You averaged only {avg_sleep}h sleep — well below the recommended 7–9h. '
                    'Poor sleep raises hunger hormones (ghrelin) and can undo nutrition progress.')
            elif avg_sleep < 7:
                recs['sleep'].append(
                    f'Your {avg_sleep}h average is close but slightly under the 7–9h optimal range. '
                    'Try a consistent bedtime 30 minutes earlier.')
            else:
                recs['sleep'].append(
                    f'Your sleep average of {avg_sleep}h is in the healthy range — keep it up!')
        else:
            recs['sleep'].append('Log your sleep in the Sleep Tracker to receive personalised sleep recommendations.')

        # Workout recommendations (based on calorie burn if available)
        recs['workout'].append(
            'Aim for at least 150 minutes of moderate aerobic activity per week (WHO guideline).')
        if user and user.get('activity_level'):
            level = float(user.get('activity_level') or 1.55)
            if level <= 1.2:
                recs['workout'].append(
                    'Your activity level is set to sedentary. Even a 20-minute daily walk can improve '
                    'insulin sensitivity and mood significantly.')
            elif level <= 1.375:
                recs['workout'].append(
                    'You exercise lightly 1–3 days/week. Adding 1–2 resistance training sessions '
                    'can boost your metabolism and protect muscle mass.')
            elif level >= 1.725:
                recs['workout'].append(
                    'Your high activity level means recovery is critical — prioritise 7–9h sleep '
                    'and 1.6–2.2g protein/kg body weight.')

        # Weight/BMI recommendations
        if cur_bmi > 0:
            if cur_bmi < 18.5:
                recs['weight'].append(
                    f'Your BMI of {cur_bmi} indicates underweight. Focus on calorie-dense, '
                    'nutrient-rich foods and consider consulting a dietitian.')
            elif cur_bmi < 25:
                recs['weight'].append(
                    f'Your BMI of {cur_bmi} is in the healthy range — maintain your current habits.')
            elif cur_bmi < 30:
                recs['weight'].append(
                    f'Your BMI of {cur_bmi} is in the overweight range. A 500 kcal/day deficit '
                    'combined with exercise can help achieve a healthy weight gradually.')
            else:
                recs['weight'].append(
                    f'Your BMI of {cur_bmi} is in the obese range. Sustainable changes — '
                    'consistent logging, increased movement, and adequate protein — are most effective.')
        else:
            recs['weight'].append('Log your weight and BMI to receive personalised weight management tips.')

        return recs

    # ──────────────────────────────────────────────────────────────────────
    # RECOMMENDATIONS PAGE  (GET /nutrition/recommendations)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def recommendations_index(cls):
        uid  = cls.uid()
        user = UserModel.find_by_id(uid)
        data_7  = cls._build_report_data(uid, 7)
        data_30 = cls._build_report_data(uid, 30)
        recs = cls._build_recommendations(uid, user, data_7)
        return cls.render('nutrition/recommendations.html',
            user=user, recs=recs,
            data_7=data_7, data_30=data_30,
            today=today_str(),
        )

    # ──────────────────────────────────────────────────────────────────────
    # MACRO TARGETS  (GET & POST /nutrition/macro-targets)
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def macro_targets_index(cls):
        uid  = cls.uid()
        user = UserModel.find_by_id(uid)
        today = today_str()
        saved = MacroTargetModel.get(uid, today)
        history = MacroTargetModel.history(uid, limit=14)

        # Auto-calc defaults from TDEE/user data if no saved targets
        auto_protein = auto_carbs = auto_fat = 0
        calorie_goal = 2000
        if user and user.get('weight_kg') and user.get('height_cm') and user.get('age'):
            try:
                wkg = float(user.get('weight_kg') or 0)
                hcm = float(user.get('height_cm') or 0)
                age = int(user.get('age') or 0)
                if wkg and hcm and age:
                    bmr = calculate_bmr(wkg, hcm, age, user.get('gender', 'male'))
                    calorie_goal = int(calculate_tdee(bmr, float(user.get('activity_level') or 1.55)))
                macros = calculate_macros(calorie_goal, user.get('fitness_goal', 'maintain'))
                auto_protein = macros.get('protein', 0)
                auto_carbs   = macros.get('carbs', 0)
                auto_fat     = macros.get('fat', 0)
            except Exception:
                pass

        # Today's actual totals
        totals = MealModel.totals(uid, today)

        return cls.render('nutrition/macro_targets.html',
            user=user,
            saved=saved,
            history=history,
            auto_protein=auto_protein,
            auto_carbs=auto_carbs,
            auto_fat=auto_fat,
            calorie_goal=calorie_goal,
            totals=totals,
            today=today,
        )

    @classmethod
    def macro_targets_save(cls):
        uid   = cls.uid()
        today = today_str()
        try:
            protein  = float(request.form.get('protein', 0))
            carbs    = float(request.form.get('carbs', 0))
            fat      = float(request.form.get('fat', 0))
            calories = float(request.form.get('calories', 2000))
        except (ValueError, TypeError):
            flash('Invalid values — please enter numbers only.', 'danger')
            return redirect(url_for('nutrition.macro_targets_index'))

        MacroTargetModel.save(uid, today, protein, carbs, fat, calories)
        NotificationModel.create(uid, 'Macro targets updated ✅',
            f'Protein {protein}g · Carbs {carbs}g · Fat {fat}g for {today}.',
            'success', '/nutrition/macro-targets')
        flash('Macro targets saved!', 'success')
        return redirect(url_for('nutrition.macro_targets_index'))

    # ──────────────────────────────────────────────────────────────────────
    # NOTIFICATIONS API
    # ──────────────────────────────────────────────────────────────────────
    @classmethod
    def notifications_list(cls):
        uid   = cls.uid()
        notifs = NotificationModel.get_for_user(uid)
        count  = NotificationModel.unread_count(uid)
        return jsonify({'notifications': [dict(n) for n in notifs], 'unread': count})

    @classmethod
    def notifications_mark_read(cls):
        uid  = cls.uid()
        nid  = request.json.get('id') if request.is_json else request.form.get('id')
        if nid == 'all':
            NotificationModel.mark_all_read(uid)
        else:
            NotificationModel.mark_read(int(nid), uid)
        return jsonify({'ok': True})

    @classmethod
    def notifications_delete(cls):
        uid = cls.uid()
        nid = request.json.get('id') if request.is_json else request.form.get('id')
        NotificationModel.delete(int(nid), uid)
        return jsonify({'ok': True})

    @classmethod
    def notifications_unread_count(cls):
        uid = cls.uid()
        return jsonify({'unread': NotificationModel.unread_count(uid)})
