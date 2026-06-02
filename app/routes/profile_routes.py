from flask import Blueprint, request
from app.controllers.profile_controller import ProfileController
from app.auth import login_required

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    return ProfileController.show_profile()

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        return ProfileController.update_profile()
    return ProfileController.edit_profile()

@profile_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    return ProfileController.show_settings()

@profile_bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    return ProfileController.change_password()

@profile_bp.route('/profile/change-password-form', methods=['GET'])
@login_required
def change_password_form():
    return ProfileController.change_password_form()