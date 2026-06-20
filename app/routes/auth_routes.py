"""app/routes/auth_routes.py — Auth URL mapping | Feature: Auth"""
from flask import Blueprint
from app.controllers.auth_controller import AuthController
from app.auth import login_required, guest_only

auth_bp = Blueprint('auth', __name__)

# ---- LOGIN (uncommented) ----
@auth_bp.route('/login', methods=['GET'])
@guest_only
def login(): return AuthController.show_login()

@auth_bp.route('/login', methods=['POST'])
def login_post(): return AuthController.process_login()

# ---- REGISTER ----
@auth_bp.route('/register', methods=['GET'])
@guest_only
def register(): return AuthController.show_register()

@auth_bp.route('/register', methods=['POST'])
def register_post(): return AuthController.process_register()

# ---- LOGOUT (uncommented) ----
@auth_bp.route('/logout')
@login_required
def logout(): return AuthController.logout()

# ---- FORGOT/RESET (uncommented) ----
@auth_bp.route('/forgot-password', methods=['GET'])
@guest_only
def forgot_password(): return AuthController.show_forgot()

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password_post(): return AuthController.process_forgot()

@auth_bp.route('/reset-password', methods=['GET'])
def reset_password(): return AuthController.show_reset()

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password_post(): return AuthController.process_reset()

# ---- GOOGLE OAuth ----
@auth_bp.route('/google')
@guest_only
def google_login(): return AuthController.google_login()

@auth_bp.route('/google/callback')
def google_callback(): return AuthController.google_callback()
# ---- PUBLIC CONTACT FORM (from homepage "Get in Touch") ----
@auth_bp.route('/contact', methods=['POST'])
def contact_form():
    from app.controllers.auth_controller import AuthController
    return AuthController.contact_form()
