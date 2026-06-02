# app/routes/dashboard_routes.py — Dashboard routes
from flask import Blueprint
from app.controllers.dashboard_controller import DashboardController
from app.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')          # <-- changed from '/dashboard' to '/'
@login_required
def index():
    return DashboardController.index()