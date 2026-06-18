"""app/routes/wellness_routes.py — Workout plans, health risk, first aid, etc."""
from flask import Blueprint
from app.auth import login_required
from app.controllers.wellness_controller import WellnessController

wellness_bp = Blueprint('wellness', __name__)

# ── Workout Plan Generator ──────────────────────────────────────────────
@wellness_bp.route('/workout-plan')
@login_required
def workout_plan():
    return WellnessController.workout_plan()

@wellness_bp.route('/workout-plan/pdf')
@login_required
def workout_plan_pdf():
    return WellnessController.workout_plan_pdf()

# ── Health Risk Predictor ───────────────────────────────────────────────
@wellness_bp.route('/health-risk')
@login_required
def health_risk():
    return WellnessController.health_risk()

# ── First Aid Guide ──────────────────────────────────────────────────────
@wellness_bp.route('/first-aid')
@login_required
def first_aid():
    return WellnessController.first_aid()

# ── Specialist Navigator ────────────────────────────────────────────────
@wellness_bp.route('/specialist-navigator')
@login_required
def specialist_navigator():
    return WellnessController.specialist_navigator()

# ── Nearby Healthcare Finder ────────────────────────────────────────────
@wellness_bp.route('/healthcare-finder')
@login_required
def healthcare_finder():
    return WellnessController.healthcare_finder()

# ── Medicine Checker ─────────────────────────────────────────────────────
@wellness_bp.route('/medicine')
@login_required
def medicine_index():
    return WellnessController.medicine_index()

@wellness_bp.route('/medicine/add', methods=['POST'])
@login_required
def medicine_add():
    return WellnessController.medicine_add()

@wellness_bp.route('/medicine/take', methods=['POST'])
@login_required
def medicine_mark_taken():
    return WellnessController.medicine_mark_taken()

@wellness_bp.route('/medicine/delete/<int:mid>', methods=['POST'])
@login_required
def medicine_delete(mid):
    return WellnessController.medicine_delete(mid)

@wellness_bp.route('/medicine/due-check')
@login_required
def medicine_due_check():
    return WellnessController.medicine_due_check()

# ── Expense Tracker ──────────────────────────────────────────────────────
@wellness_bp.route('/expenses')
@login_required
def expense_index():
    return WellnessController.expense_index()

@wellness_bp.route('/expenses/add', methods=['POST'])
@login_required
def expense_add():
    return WellnessController.expense_add()

@wellness_bp.route('/expenses/delete/<int:eid>', methods=['POST'])
@login_required
def expense_delete(eid):
    return WellnessController.expense_delete(eid)

@wellness_bp.route('/expenses/pdf')
@login_required
def expense_pdf():
    return WellnessController.expense_pdf()

# ── Support / Contact Admin ──────────────────────────────────────────────
@wellness_bp.route('/support')
@login_required
def support_index():
    return WellnessController.support_index()

@wellness_bp.route('/support/send', methods=['POST'])
@login_required
def support_send():
    return WellnessController.support_send()
