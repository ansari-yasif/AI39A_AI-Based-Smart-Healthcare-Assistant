"""app/controllers/admin_controller.py — Admin control panel
User management, support messages, outbreak alerts."""
from flask import request, redirect, url_for, flash
from app.controllers.base_controller import BaseController
from app.models.user import UserModel
from app.models.support import SupportModel
from app.models.outbreak import OutbreakModel
from app.models.notification import NotificationModel


class AdminController(BaseController):

    # ════════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def dashboard(cls):
        try: total_users = UserModel.count_all()
        except: total_users = 0
        try: active_today = UserModel.count_active_today()
        except: active_today = 0
        try: new_this_week = UserModel.count_new_this_week()
        except: new_this_week = 0
        try: open_messages = SupportModel.unread_count()
        except: open_messages = 0
        try: recent_users = (UserModel.get_all_detailed() or [])[:5]
        except: recent_users = []
        try: recent_messages = (SupportModel.all_messages() or [])[:5]
        except: recent_messages = []

        stats = {
            'total_users': total_users,
            'active_today': active_today,
            'new_this_week': new_this_week,
            'open_messages': open_messages,
        }
        return cls.render('admin/dashboard.html',
            stats=stats, recent_users=recent_users, recent_messages=recent_messages)

    # ════════════════════════════════════════════════════════════════════
    # USER MANAGEMENT
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def users_index(cls):
        search = request.args.get('q', '').strip()
        users = UserModel.get_all_detailed(search)
        return cls.render('admin/list_users.html', users=users, search=search)

    @classmethod
    def user_edit(cls, uid):
        user = UserModel.find_by_id(uid)
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('admin.users_index'))
        if request.method == 'POST':
            full_name = request.form.get('full_name', '').strip()
            email = request.form.get('email', '').strip().lower()
            role = request.form.get('role', 'user')
            is_active = 1 if request.form.get('is_active') == 'on' else 0
            UserModel.admin_update(uid, full_name, email, role, is_active)
            flash(f'User {full_name} updated.', 'success')
            return redirect(url_for('admin.users_index'))
        return cls.render('admin/edit_user.html', user=user)

    @classmethod
    def user_toggle_active(cls, uid):
        user = UserModel.find_by_id(uid)
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('admin.users_index'))
        new_status = 0 if user.get('is_active', 1) else 1
        UserModel.set_active(uid, new_status)
        status_txt = 'activated' if new_status else 'deactivated'
        flash(f'User {status_txt}.', 'success')
        return redirect(url_for('admin.users_index'))

    @classmethod
    def user_delete(cls, uid):
        from flask import session
        my_id = session.get('user_id')
        if str(my_id) == str(uid):
            flash('You cannot delete your own account.', 'danger')
            return redirect(url_for('admin.users_index'))
        try:
            user = UserModel.find_by_id(uid)
            if not user:
                flash('User not found.', 'danger')
                return redirect(url_for('admin.users_index'))
            name = user.get('full_name', f'User #{uid}')
            UserModel.admin_delete(uid)
            flash(f'User "{name}" and all their data have been deleted.', 'success')
        except Exception as e:
            flash(f'Delete failed: {str(e)[:100]}', 'danger')
        return redirect(url_for('admin.users_index'))

    @classmethod
    def add_user_form(cls):
        return cls.render('admin/add_user.html')

    @classmethod
    def add_user_submit(cls):
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'user')

        if not full_name or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('admin.add_user_form'))
        if UserModel.email_exists(email):
            flash('Email already registered.', 'danger')
            return redirect(url_for('admin.add_user_form'))

        UserModel.create(full_name, email, password)
        # Promote to admin if requested
        if role == 'admin':
            new_user = UserModel.find_by_email(email)
            if new_user:
                UserModel.admin_update(new_user['id'], full_name, email, 'admin', 1)
        flash(f'User {full_name} created.', 'success')
        return redirect(url_for('admin.users_index'))

    # ════════════════════════════════════════════════════════════════════
    # SUPPORT MESSAGES (from users)
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def messages_index(cls):
        status = request.args.get('status', '').strip()
        try:
            msgs = SupportModel.all_messages(status if status else None) or []
        except Exception as e:
            msgs = []
            flash(f'Could not load messages: {e}', 'warning')
        return cls.render('admin/messages.html', messages=msgs, status=status)

    @classmethod
    def message_view(cls, mid):
        msg = SupportModel.get_one(mid)
        if not msg:
            flash('Message not found.', 'danger')
            return redirect(url_for('admin.messages_index'))
        if request.method == 'POST':
            reply = request.form.get('reply', '').strip()
            if reply:
                SupportModel.reply(mid, reply)
                NotificationModel.create(msg['user_id'], f'Admin replied to "{msg["subject"]}" 📩',
                    reply[:150], 'info', '/wellness/support')
                flash('Reply sent.', 'success')
            return redirect(url_for('admin.messages_index'))
        return cls.render('admin/message_view.html', msg=msg)

    @classmethod
    def message_close(cls, mid):
        SupportModel.close(mid)
        flash('Message closed.', 'info')
        return redirect(url_for('admin.messages_index'))

    # ════════════════════════════════════════════════════════════════════
    # OUTBREAK ALERTS
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def outbreaks_index(cls):
        alerts = OutbreakModel.all_alerts()
        return cls.render('admin/outbreaks.html', alerts=alerts)

    @classmethod
    def outbreak_create(cls):
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        severity = request.form.get('severity', 'medium')
        region = request.form.get('region', '').strip()
        expires = request.form.get('expires_at', '') or None
        if not title:
            flash('Title is required.', 'danger')
            return redirect(url_for('admin.outbreaks_index'))
        OutbreakModel.create(title, description, severity, region, expires)
        flash('Outbreak alert created and is now visible to all users.', 'success')
        return redirect(url_for('admin.outbreaks_index'))

    @classmethod
    def outbreak_deactivate(cls, aid):
        OutbreakModel.deactivate(aid)
        flash('Alert deactivated.', 'info')
        return redirect(url_for('admin.outbreaks_index'))

    @classmethod
    def outbreak_delete(cls, aid):
        OutbreakModel.delete(aid)
        flash('Alert deleted.', 'info')
        return redirect(url_for('admin.outbreaks_index'))
