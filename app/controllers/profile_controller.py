"""app/controllers/profile_controller.py — User profile | Feature: Profile"""
from flask import session, request
from app.controllers.base_controller import BaseController
from app.models.user import UserModel
from app.auth import verify_password
from app.helpers import is_strong_password, sanitize
from app.constants import ACTIVITY_LEVELS


class ProfileController(BaseController):

    # Calculate profile completion percentage
    @classmethod
    def profile_completion(cls):
        uid = cls.uid()
        user = UserModel.find_by_id(uid)

        fields = [
            user.get('full_name'),
            user.get('phone'),
            user.get('bio'),
            user.get('age'),
            user.get('weight_kg'),
            user.get('height_cm'),
            user.get('gender')
        ]

        completed = sum(1 for field in fields if field)
        percentage = int((completed / len(fields)) * 100)

        return percentage

    # Show profile page (main)
    @classmethod
    def show_profile(cls):
        uid = cls.uid()
        user = UserModel.find_by_id(uid)
        completion = cls.profile_completion()

        return cls.render(
            'profile/profile.html',
            user=user,
            completion=completion
        )

    # Show edit profile form (GET)
    @classmethod
    def edit_profile(cls):
        uid = cls.uid()
        user = UserModel.find_by_id(uid)
        return cls.render('profile/edit_profile.html', user=user)

    # Process profile update (POST)
    @classmethod
    def update_profile(cls):
        uid = cls.uid()
        name = sanitize(request.form.get('full_name', ''))
        phone = sanitize(request.form.get('phone', ''))
        bio = sanitize(request.form.get('bio', ''))

        if not name:
            cls.flash_err('Name is required.')
            return cls.redirect_to('profile.edit_profile')

        UserModel.update_profile(uid, name, phone, bio)

        age = cls.form_int('age')
        weight = cls.form_float('weight_kg')
        height = cls.form_float('height_cm')
        activity = cls.form_float('activity_level', 1.55)
        gender = request.form.get('gender', 'male')
        goal = request.form.get('goal', 'maintain')

        if age and weight and height:
            UserModel.update_health(uid, age, gender, weight, height, goal, activity)

        session['full_name'] = name
        cls.flash_ok('Profile updated successfully!')
        return cls.redirect_to('profile.profile')

    # Show change password form (GET)
    @classmethod
    def change_password_form(cls):
        return cls.render('profile/change_password.html')

    # Process password change (POST)
    @classmethod
    def change_password(cls):
        uid = cls.uid()
        current = request.form.get('current_password')
        new_pwd = request.form.get('new_password')
        confirm = request.form.get('confirm_password')

        user = UserModel.find_by_id(uid)

        if user.get('password_hash'):
            if not verify_password(current, user['password_hash']):
                cls.flash_err('Current password is incorrect.')
                return cls.redirect_to('profile.change_password')
        else:
            if current:
                cls.flash_err('You signed in with Google. Just enter a new password.')
                return cls.redirect_to('profile.change_password')

        if not is_strong_password(new_pwd):
            cls.flash_err('Password needs 8+ characters, uppercase, lowercase and a number.')
            return cls.redirect_to('profile.change_password')

        if new_pwd != confirm:
            cls.flash_err('Passwords do not match.')
            return cls.redirect_to('profile.change_password')

        UserModel.update_password(uid, new_pwd)
        cls.flash_ok('Password changed successfully!')
        return cls.redirect_to('profile.profile')

    # Settings page of user profile
    @classmethod
    def show_settings(cls):
        return cls.render('settings.html')