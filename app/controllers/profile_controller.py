"""app/controllers/profile_controller.py — User profile | Feature: Profile"""
from flask import session, request, redirect, url_for, flash
from app.controllers.base_controller import BaseController
from app.models.user import UserModel
from app.auth import verify_password
from app.helpers import is_strong_password, sanitize
from app.constants import ACTIVITY_LEVELS


class ProfileController(BaseController):

    # ---------- Helper ----------
    @classmethod
    def _get_user_or_redirect(cls):
        """Fetch the logged-in user; if not found, redirect to login with error."""
        uid = cls.uid()
        if not uid:
            flash('Please log in to access your profile.', 'warning')
            return None, redirect(url_for('auth.login'))
        
        user = UserModel.find_by_id(uid)
        if not user:
            flash('User account not found. Please log in again.', 'danger')
            return None, redirect(url_for('auth.login'))
        
        return user, None  # (user, redirect_response) – redirect_response is None when OK

    # ---------- Profile page ----------
    @classmethod
    def show_profile(cls):
        user, redirect_resp = cls._get_user_or_redirect()
        if redirect_resp:
            return redirect_resp
        return cls.render('profile/profile.html', user=user)

    # ---------- Edit profile form ----------
    @classmethod
    def edit_profile(cls):
        user, redirect_resp = cls._get_user_or_redirect()
        if redirect_resp:
            return redirect_resp
        return cls.render('profile/edit_profile.html', user=user)

    # ---------- Update profile (POST) ----------
    @classmethod
    def update_profile(cls):
        user, redirect_resp = cls._get_user_or_redirect()
        if redirect_resp:
            return redirect_resp

        uid = cls.uid()  # safe because _get_user_or_redirect already checked
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

    # ---------- Change password form ----------
    @classmethod
    def change_password_form(cls):
        user, redirect_resp = cls._get_user_or_redirect()
        if redirect_resp:
            return redirect_resp
        return cls.render('profile/change_password.html')

    # ---------- Change password (POST) ----------
    @classmethod
    def change_password(cls):
        user, redirect_resp = cls._get_user_or_redirect()
        if redirect_resp:
            return redirect_resp

        uid = cls.uid()
        current = request.form.get('current_password')
        new_pwd = request.form.get('new_password')
        confirm = request.form.get('confirm_password')

        # user is guaranteed to be a dict (not None) here
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

    # ---------- Settings page ----------
    @classmethod
    def show_settings(cls):
        user, redirect_resp = cls._get_user_or_redirect()
        if redirect_resp:
            return redirect_resp
        return cls.render('settings.html')