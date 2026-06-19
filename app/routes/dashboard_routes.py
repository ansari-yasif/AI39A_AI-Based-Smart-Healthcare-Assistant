# app/routes/dashboard_routes.py — Dashboard routes
from flask import Blueprint
from app.controllers.dashboard_controller import DashboardController
from app.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')          # <-- changed from '/dashboard' to '/'
@login_required
def index():
    return DashboardController.index()
@dashboard_bp.route('/notifications/json')
@login_required
def notifications_json():
    return DashboardController.notifications_json()

@dashboard_bp.route('/notifications/mark-read', methods=['POST'])
@login_required
def notifications_mark_read():
    return DashboardController.notifications_mark_read()

@dashboard_bp.route('/notifications/mark-all-read', methods=['POST'])
@login_required
def notifications_mark_all_read():
    return DashboardController.notifications_mark_all_read()
