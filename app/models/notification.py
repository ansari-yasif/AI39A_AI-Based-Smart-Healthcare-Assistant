"""app/models/notification.py — Notifications model"""
from app.models.base_model import BaseModel


class NotificationModel(BaseModel):
    TABLE = 'notifications'

    @classmethod
    def create(cls, uid, title, body='', ntype='info', link=None):
        return cls.execute(
            'INSERT INTO notifications(user_id,title,body,type,link,created_at) VALUES(%s,%s,%s,%s,%s,NOW())',
            (uid, title, body, ntype, link)
        )

    @classmethod
    def get_for_user(cls, uid, limit=20):
        return cls.fetch_all(
            'SELECT * FROM notifications WHERE user_id=%s ORDER BY created_at DESC LIMIT %s',
            (uid, limit)
        )

    @classmethod
    def unread_count(cls, uid):
        row = cls.fetch_one(
            'SELECT COUNT(*) AS cnt FROM notifications WHERE user_id=%s AND is_read=0',
            (uid,)
        )
        return int(row['cnt']) if row else 0

    @classmethod
    def mark_read(cls, nid, uid):
        return cls.execute(
            'UPDATE notifications SET is_read=1 WHERE id=%s AND user_id=%s', (nid, uid)
        )

    @classmethod
    def mark_all_read(cls, uid):
        return cls.execute(
            'UPDATE notifications SET is_read=1 WHERE user_id=%s AND is_read=0', (uid,)
        )

    @classmethod
    def delete(cls, nid, uid):
        return cls.execute(
            'DELETE FROM notifications WHERE id=%s AND user_id=%s', (nid, uid)
        )

    @classmethod
    def ensure_welcome(cls, uid):
        """Create welcome notification for new users if none exist."""
        existing = cls.fetch_one('SELECT id FROM notifications WHERE user_id=%s LIMIT 1', (uid,))
        if not existing:
            cls.create(uid, 'Welcome to VitaPulse! 🎉',
                       'Start by completing your health profile to unlock BMR, TDEE and macro targets.',
                       'info', '/profile/edit')
            cls.create(uid, 'Set your daily calorie goal 🎯',
                       'Visit the Calorie Calculator to set a personalised daily goal.',
                       'tip', '/nutrition/calories')
