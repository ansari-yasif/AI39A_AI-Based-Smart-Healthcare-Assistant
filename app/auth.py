"""app/auth.py — Auth decorators + session/password helpers"""
import functools
from flask import session, redirect, url_for, flash, abort, request
from werkzeug.security import generate_password_hash, check_password_hash


# ── Decorators ────────────────────────────────────────────────

def login_required(fn):
    """Block unauthenticated users → redirect to login."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    """Block non-admin users → 403."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


def guest_only(fn):
    """Redirect already-logged-in users to dashboard."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return redirect(url_for('dashboard.index'))
        return fn(*args, **kwargs)
    return wrapper


# ── Session helpers ───────────────────────────────────────────

def login_user(user: dict):
    session.permanent = True
    session['user_id']   = user['id']
    session['full_name'] = user['full_name']
    session['email']     = user['email']
    session['role']      = user.get('role', 'user')
    session['avatar']    = user.get('avatar_url', '')


def logout_user():
    session.clear()


def current_user() -> dict:
    if 'user_id' not in session:
        return {}
    return {
        'id':        session.get('user_id'),
        'full_name': session.get('full_name', ''),
        'email':     session.get('email', ''),
        'role':      session.get('role', 'user'),
        'avatar':    session.get('avatar', ''),
    }


def is_authenticated() -> bool:
    return 'user_id' in session


# ── Password helpers ──────────────────────────────────────────

def hash_password(plain: str) -> str:
    return generate_password_hash(plain, method='pbkdf2:sha256', salt_length=16)


def verify_password(plain: str, hashed: str) -> bool:
    return check_password_hash(hashed, plain)
