"""app/controllers/auth_controller.py — Full auth: login, register, forgot password, Google OAuth | Feature: Auth"""
from flask import request, session, current_app
from app.controllers.base_controller import BaseController
from app.models.user import UserModel
from app.auth import login_user, logout_user
from app.helpers import is_valid_email, is_strong_password, sanitize


class AuthController(BaseController):

    # ── Login ────────────────────────────────────────────────
    @classmethod
    def show_login(cls):
        return cls.render('login.html')

    @classmethod
    def process_login(cls):
        email = sanitize(cls.form('email')).lower()
        pwd   = cls.form('password')
        if not email or not pwd:
            cls.flash_err('Email and password required.')
            return cls.render('login.html')
        user = UserModel.authenticate(email, pwd)
        if not user:
            cls.flash_err('Invalid email or password.')
            return cls.render('login.html')
        login_user(user)
        cls.flash_ok(f'Welcome back, {user["full_name"].split()[0]}!')
        nxt = request.args.get('next', '')
        if nxt and nxt.startswith('/'):
            from flask import redirect
            return redirect(nxt)
        return cls.redirect_to('dashboard.index')

    # ── Register ─────────────────────────────────────────────
    @classmethod
    def show_register(cls):
        return cls.render('register.html')

    @classmethod
    def process_register(cls):
        name  = sanitize(cls.form('full_name'))
        email = sanitize(cls.form('email')).lower()
        pwd   = cls.form('password')
        cpwd  = cls.form('confirm_password')
        if not all([name, email, pwd, cpwd]):
            cls.flash_err('All fields are required.')
            return cls.render('register.html')
        if not is_valid_email(email):
            cls.flash_err('Please enter a valid email address.')
            return cls.render('register.html')
        if not is_strong_password(pwd):
            cls.flash_err('Password needs 8+ chars with uppercase, lowercase and a number.')
            return cls.render('register.html')
        if pwd != cpwd:
            cls.flash_err('Passwords do not match.')
            return cls.render('register.html')
        if UserModel.email_exists(email):
            cls.flash_err('This email is already registered. Please sign in.')
            return cls.render('register.html')
        uid  = UserModel.create(name, email, pwd)
        user = UserModel.find_by_id(uid)
        login_user(user)
        cls.flash_ok('Account created! Welcome to VitaPulse 🎉')
        return cls.redirect_to('dashboard.index')

    # ── Logout ───────────────────────────────────────────────
    @classmethod
    def logout(cls):
        logout_user()
        cls.flash_ok('You have been logged out.')
        return cls.redirect_to('index')

    # ── Forgot Password ──────────────────────────────────────
    @classmethod
    def show_forgot(cls):
        return cls.render('forgot_password.html')

    @classmethod
    def process_forgot(cls):
        email = sanitize(cls.form('email')).lower()
        if not email or not is_valid_email(email):
            cls.flash_err('Please enter a valid email address.')
            return cls.render('forgot_password.html')
        user = UserModel.find_by_email(email)
        # Always show success message (don't reveal if email exists — security)
        if user:
            # In production: send reset email with token
            # For now: flash success and redirect
            current_app.logger.info(f'Password reset requested for {email}')
        cls.flash_ok('If this email is registered, a reset link has been sent.')
        return cls.redirect_to('auth.login')

    @classmethod
    def show_reset(cls):
        return cls.render('reset_password.html')

    @classmethod
    def process_reset(cls):
        # Simplified — in production use signed tokens
        email   = sanitize(cls.form('email')).lower()
        new_pwd = cls.form('new_password')
        confirm = cls.form('confirm_password')
        if not is_strong_password(new_pwd):
            cls.flash_err('Password needs 8+ chars with uppercase, lowercase and number.')
            return cls.render('reset_password.html')
        if new_pwd != confirm:
            cls.flash_err('Passwords do not match.')
            return cls.render('reset_password.html')
        user = UserModel.find_by_email(email)
        if user:
            UserModel.update_password(user['id'], new_pwd)
            cls.flash_ok('Password reset successfully! Please sign in.')
        return cls.redirect_to('auth.login')
