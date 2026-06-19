"""app/routes/nutrition_routes.py — Nutrition URL mapping (MVC Routes)"""
from flask import Blueprint
from app.controllers.nutrition_controller import NutritionController
from app.auth import login_required

nutrition_bp = Blueprint('nutrition', __name__)

# ── Calorie Calculator ─────────────────────────────────────────────────────
@nutrition_bp.route('/calories')
@login_required
def calorie_index():
    return NutritionController.calorie_index()

@nutrition_bp.route('/calories/goal', methods=['POST'])
@login_required
def update_goal():
    return NutritionController.update_goal()

# ── Meal Tracker ───────────────────────────────────────────────────────────
@nutrition_bp.route('/meals')
@login_required
def meal_index():
    return NutritionController.meal_index()

@nutrition_bp.route('/meals/add', methods=['POST'])
@login_required
def add_meal():
    return NutritionController.add_meal()

@nutrition_bp.route('/meals/delete/<int:meal_id>', methods=['POST'])
@login_required
def delete_meal(meal_id):
    return NutritionController.delete_meal(meal_id)

# ── Food Database ──────────────────────────────────────────────────────────
@nutrition_bp.route('/foods')
@login_required
def food_db_index():
    return NutritionController.food_db_index()

@nutrition_bp.route('/foods/search')
@login_required
def food_search_api():
    return NutritionController.food_search_api()

@nutrition_bp.route('/foods/quick-add', methods=['POST'])
@login_required
def quick_add_to_meal():
    return NutritionController.quick_add_to_meal()

# ── Custom Foods ───────────────────────────────────────────────────────────
@nutrition_bp.route('/foods/custom/add', methods=['POST'])
@login_required
def add_custom_food():
    return NutritionController.add_custom_food()

@nutrition_bp.route('/foods/custom/delete/<int:cid>', methods=['POST'])
@login_required
def delete_custom_food(cid):
    return NutritionController.delete_custom_food(cid)

# ── BMI Calculator ─────────────────────────────────────────────────────────
@nutrition_bp.route('/bmi')
@login_required
def bmi_index():
    return NutritionController.bmi_index()

@nutrition_bp.route('/bmi/calculate', methods=['POST'])
@login_required
def bmi_calculate():
    return NutritionController.bmi_calculate()

# ── Reports ────────────────────────────────────────────────────────────────
@nutrition_bp.route('/reports')
@login_required
def reports_index():
    return NutritionController.reports_index()

@nutrition_bp.route('/reports/weekly/pdf')
@login_required
def weekly_report_pdf():
    return NutritionController.weekly_report_pdf()

@nutrition_bp.route('/reports/monthly/pdf')
@login_required
def monthly_report_pdf():
    return NutritionController.monthly_report_pdf()

# ── Personalised Recommendations ───────────────────────────────────────────
@nutrition_bp.route('/recommendations')
@login_required
def recommendations_index():
    return NutritionController.recommendations_index()

# ── Macro Targets ──────────────────────────────────────────────────────────
@nutrition_bp.route('/macro-targets')
@login_required
def macro_targets_index():
    return NutritionController.macro_targets_index()

@nutrition_bp.route('/macro-targets/save', methods=['POST'])
@login_required
def macro_targets_save():
    return NutritionController.macro_targets_save()

# ── Notifications API ──────────────────────────────────────────────────────
@nutrition_bp.route('/notifications')
@login_required
def notifications_list():
    return NutritionController.notifications_list()

@nutrition_bp.route('/notifications/read', methods=['POST'])
@login_required
def notifications_mark_read():
    return NutritionController.notifications_mark_read()

@nutrition_bp.route('/notifications/delete', methods=['POST'])
@login_required
def notifications_delete():
    return NutritionController.notifications_delete()

@nutrition_bp.route('/notifications/count')
@login_required
def notifications_unread_count():
    return NutritionController.notifications_unread_count()
