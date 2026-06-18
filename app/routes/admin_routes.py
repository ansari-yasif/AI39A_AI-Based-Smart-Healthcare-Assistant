"""app/routes/admin_routes.py — Admin control panel URLs"""
from flask import Blueprint
from app.auth import admin_required
from app.controllers.admin_controller import AdminController

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@admin_required
def dashboard():
    return AdminController.dashboard()

# ── Users ────────────────────────────────────────────────────────────────
@admin_bp.route('/users')
@admin_required
def users_index():
    return AdminController.users_index()

@admin_bp.route('/users/add', methods=['GET'])
@admin_required
def add_user_form():
    return AdminController.add_user_form()

@admin_bp.route('/users/add', methods=['POST'])
@admin_required
def add_user_submit():
    return AdminController.add_user_submit()

@admin_bp.route('/users/<int:uid>/edit', methods=['GET', 'POST'])
@admin_required
def user_edit(uid):
    return AdminController.user_edit(uid)

@admin_bp.route('/users/<int:uid>/toggle', methods=['POST'])
@admin_required
def user_toggle_active(uid):
    return AdminController.user_toggle_active(uid)

@admin_bp.route('/users/<int:uid>/delete', methods=['POST'])
@admin_required
def user_delete(uid):
    return AdminController.user_delete(uid)

# ── Support messages ─────────────────────────────────────────────────────
@admin_bp.route('/messages')
@admin_required
def messages_index():
    return AdminController.messages_index()

@admin_bp.route('/messages/<int:mid>', methods=['GET', 'POST'])
@admin_required
def message_view(mid):
    return AdminController.message_view(mid)

@admin_bp.route('/messages/<int:mid>/close', methods=['POST'])
@admin_required
def message_close(mid):
    return AdminController.message_close(mid)

# ── Outbreak alerts ───────────────────────────────────────────────────────
@admin_bp.route('/outbreaks')
@admin_required
def outbreaks_index():
    return AdminController.outbreaks_index()

@admin_bp.route('/outbreaks/create', methods=['POST'])
@admin_required
def outbreak_create():
    return AdminController.outbreak_create()

@admin_bp.route('/outbreaks/<int:aid>/deactivate', methods=['POST'])
@admin_required
def outbreak_deactivate(aid):
    return AdminController.outbreak_deactivate(aid)

@admin_bp.route('/outbreaks/<int:aid>/delete', methods=['POST'])
@admin_required
def outbreak_delete(aid):
    return AdminController.outbreak_delete(aid)
