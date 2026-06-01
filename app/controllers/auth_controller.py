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
        # Pass empty dicts to prevent UndefinedError
        return cls.render('register.html', errors={}, form_data={})

    @classmethod
    def process_register(cls):
        name = sanitize(cls.form('full_name')).strip()
        email = sanitize(cls.form('email')).lower().strip()
        pwd = cls.form('password')
        cpwd = cls.form('confirm_password')
        terms = cls.form('terms')

        errors = {}
        form_data = {
            'full_name': name,
            'email': email,
            'terms': terms
        }

        # Name validation
        if not name:
            errors['full_name'] = 'Full name is required.'

        # Email validation
        if not email:
            errors['email'] = 'Email address is required.'
        elif not is_valid_email(email):
            errors['email'] = 'Please enter a valid email address (e.g., name@example.com).'

        # Password validation
        if not pwd:
            errors['password'] = 'Password is required.'
        elif not is_strong_password(pwd):
            errors['password'] = 'Password needs 8+ characters with uppercase, lowercase and a number.'

        # Confirm password
        if not cpwd:
            errors['confirm_password'] = 'Please confirm your password.'
        elif pwd != cpwd:
            errors['confirm_password'] = 'Passwords do not match.'

        # Terms checkbox
        if not terms:
            errors['terms'] = 'You must agree to the Terms of Service and Privacy Policy.'

        # Email uniqueness (only if email is valid so far)
        if not errors.get('email') and UserModel.email_exists(email):
            errors['email'] = 'This email is already registered. Please sign in.'

        # If any errors, re-render with error messages and preserved data
        if errors:
            return cls.render('register.html', errors=errors, form_data=form_data)

        # Create user (password hashing inside UserModel.create)
        uid = UserModel.create(name, email, pwd)
        if not uid:
            cls.flash_err('Registration failed. Please try again.')
            return cls.render('register.html', errors={}, form_data=form_data)

        cls.flash_ok('Account created successfully! Please log in with your credentials.')
        return cls.redirect_to('auth.login')

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
        if user:
            current_app.logger.info(f'Password reset requested for {email}')
        cls.flash_ok('If this email is registered, a reset link has been sent.')
        return cls.redirect_to('auth.login')

    @classmethod
    def show_reset(cls):
        return cls.render('reset_password.html')

    @classmethod
    def process_reset(cls):
        email = sanitize(cls.form('email')).lower()
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