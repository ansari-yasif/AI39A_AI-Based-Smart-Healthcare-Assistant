"""app/controllers/auth_controller.py — Fixed Google OAuth with global oauth"""
from flask import request, session, current_app, redirect, url_for
from app.controllers.base_controller import BaseController
from app.models.user import UserModel
try:
    from app.models.notification import NotificationModel as _NM
except Exception:
    _NM = None
from app.auth import login_user, logout_user
from app.helpers import is_valid_email, is_strong_password, sanitize
from app import oauth  # Import the global OAuth object
import secrets
import logging

logger = logging.getLogger(__name__)


class AuthController(BaseController):

    # ── Login ────────────────────────────────────────────────
    @classmethod
    def show_login(cls):
        return cls.render('login.html')

    @classmethod
    def process_login(cls):
        email = sanitize(cls.form('email')).lower()
        pwd = cls.form('password')
        if not email or not pwd:
            cls.flash_err('Email and password required.')
            return cls.render('login.html')
        user = UserModel.authenticate(email, pwd)
        if not user:
            cls.flash_err('Invalid email or password.')
            return cls.render('login.html')
        # Handle case where column might be missing or set to 0
        if user.get('is_active') is not None and user.get('is_active') == 0:
            cls.flash_err('Your account has been deactivated. Please contact support.')
            return cls.render('login.html')
        login_user(user)
        session.permanent = True   # <-- ADD THIS LINE (makes session survive browser restart)
        cls.flash_ok(f'Welcome back, {user["full_name"].split()[0]}!')
        nxt = request.args.get('next', '')
        if nxt and nxt.startswith('/'):
            return redirect(nxt)
        return cls.redirect_to('dashboard.index')

    # ── Register ─────────────────────────────────────────────
    @classmethod
    def show_register(cls):
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

        if not name:
            errors['full_name'] = 'Full name is required.'
        if not email:
            errors['email'] = 'Email address is required.'
        elif not is_valid_email(email):
            errors['email'] = 'Please enter a valid email address (e.g., name@example.com).'
        if not pwd:
            errors['password'] = 'Password is required.'
        elif not is_strong_password(pwd):
            errors['password'] = 'Password needs 8+ chars with uppercase, lowercase and a number.'
        if not cpwd:
            errors['confirm_password'] = 'Please confirm your password.'
        elif pwd != cpwd:
            errors['confirm_password'] = 'Passwords do not match.'
        if not terms:
            errors['terms'] = 'You must agree to the Terms of Service and Privacy Policy.'

        if not errors.get('email') and UserModel.email_exists(email):
            errors['email'] = 'This email is already registered. Please sign in.'

        if errors:
            return cls.render('register.html', errors=errors, form_data=form_data)

        uid = UserModel.create(name, email, pwd)
        if not uid:
            cls.flash_err('Registration failed. Please try again.')
            return cls.render('register.html', errors={}, form_data=form_data)

        cls.flash_ok('Account created successfully! Please log in with your credentials.')
        return cls.redirect_to('auth.login')

    # ── Google OAuth (with full exception handling) ──────────
    @classmethod
    def google_login(cls):
        """Step 1: Redirect user to Google consent screen"""
        try:
            # Generate a random state token for CSRF protection
            state = secrets.token_urlsafe(32)
            session['oauth_state'] = state

            # Use Flask's url_for to get the absolute callback URL
            redirect_uri = url_for('auth.google_callback', _external=True)

            # Pass the state parameter to Google
            return oauth.google.authorize_redirect(redirect_uri, state=state)

        except Exception as e:
            current_app.logger.error(f'Google login init error: {str(e)}', exc_info=True)
            cls.flash_err('Unable to start Google sign‑in. Please try again later.')
            return redirect(url_for('auth.login'))

    @classmethod
    def google_callback(cls):
        """Step 2: Handle Google's callback and log in the user"""
        # Validate state to prevent CSRF
        stored_state = session.pop('oauth_state', None)
        request_state = request.args.get('state')
        if not stored_state or stored_state != request_state:
            current_app.logger.error(f'State mismatch: stored={stored_state}, received={request_state}')
            cls.flash_err('Security validation failed. Please try again.')
            return redirect(url_for('auth.login'))

        try:
            # Fetch access token
            token = oauth.google.authorize_access_token()

            # Get user info from Google UserInfo endpoint
            resp = oauth.google.get('https://www.googleapis.com/oauth2/v3/userinfo')
            if resp.status_code != 200:
                current_app.logger.error(f'Google userinfo failed: {resp.status_code} - {resp.text}')
                cls.flash_err('Could not retrieve your profile from Google. Please try again.')
                return redirect(url_for('auth.login'))

            user_info = resp.json()
            email = user_info.get('email', '').lower()
            full_name = user_info.get('name', '')
            avatar = user_info.get('picture', '')

            if not email:
                cls.flash_err('Google login failed: no email provided.')
                return redirect(url_for('auth.login'))

            user = UserModel.find_by_email(email)

            if user:
                login_user(user)
                session.permanent = True   # <-- ADD THIS LINE
                cls.flash_ok(f'Welcome back, {user["full_name"].split()[0]}!')
                return redirect(url_for('dashboard.index'))
            else:
                # Create a new account with a random password (user will use Google only)
                temp_password = secrets.token_urlsafe(16)
                uid = UserModel.create(full_name, email, temp_password)
                if uid:
                    user = UserModel.find_by_id(uid)
                    login_user(user)
                    session.permanent = True   # <-- ADD THIS LINE
                    cls.flash_ok('Account created with Google! Welcome to VitaPulse 🎉')
                    return redirect(url_for('dashboard.index'))
                else:
                    cls.flash_err('Could not create account. Please try again.')
                    return redirect(url_for('auth.register'))

        except Exception as e:
            current_app.logger.error(f'Google OAuth callback error: {str(e)}', exc_info=True)
            cls.flash_err('Google authentication failed. Please try again.')
            return redirect(url_for('auth.login'))

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
    @classmethod
    def contact_form(cls):
        """Public contact form from homepage — saves to support_messages with user_id=0."""
        from flask import request, redirect, url_for, flash, jsonify
        from app.models.support import SupportModel
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not full_name or not email or not message:
            flash('All fields are required.', 'danger')
            return redirect(url_for('index') + '#contact-section')

        # Save as guest message (user_id=0) with name/email in subject
        subject = f"[Website] Message from {full_name} <{email}>"
        SupportModel.create_guest(full_name, email, subject, message)
        flash('Thank you! Your message has been sent. We will get back to you soon.', 'success')
        return redirect(url_for('index') + '#contact-section')
