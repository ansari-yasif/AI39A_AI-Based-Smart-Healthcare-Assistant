"""app/routes/health_routes.py — Health tracker URLs"""
from flask import Blueprint
from app.auth import login_required
from app.controllers.health_controller import HealthController

health_bp = Blueprint('health', __name__)

# ── Sleep ──────────────────────────────────────────────────────────────────
@health_bp.route('/sleep')
@login_required
def sleep_index():
    return HealthController.sleep_index()

@health_bp.route('/sleep/log', methods=['POST'])
@login_required
def sleep_log():
    return HealthController.sleep_log()

@health_bp.route('/sleep/delete/<int:sid>', methods=['POST'])
@login_required
def sleep_delete(sid):
    return HealthController.sleep_delete(sid)

# ── Mood ───────────────────────────────────────────────────────────────────
@health_bp.route('/mood')
@login_required
def mood_index():
    return HealthController.mood_index()

@health_bp.route('/mood/log', methods=['POST'])
@login_required
def mood_log():
    return HealthController.mood_log()

# ── Weight ─────────────────────────────────────────────────────────────────
@health_bp.route('/weight')
@login_required
def weight_index():
    return HealthController.weight_index()

@health_bp.route('/weight/log', methods=['POST'])
@login_required
def weight_log():
    return HealthController.weight_log()

# ── Workout ────────────────────────────────────────────────────────────────
@health_bp.route('/workout')
@login_required
def workout_index():
    return HealthController.workout_index()

@health_bp.route('/workout/log', methods=['POST'])
@login_required
def workout_log():
    return HealthController.workout_log()

@health_bp.route('/workout/delete/<int:wid>', methods=['POST'])
@login_required
def workout_delete(wid):
    return HealthController.workout_delete(wid)
