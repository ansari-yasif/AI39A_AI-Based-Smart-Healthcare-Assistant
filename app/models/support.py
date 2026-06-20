"""app/models/support.py — Support messages to admin"""
from app.models.base_model import BaseModel


class SupportModel(BaseModel):
    TABLE = 'support_messages'

    # ── User sends a support message ────────────────────────────────────────
    @classmethod
    def create(cls, uid, subject, message):
        try:
            return cls.execute(
                'INSERT INTO support_messages(user_id,subject,message,status,created_at) '
                'VALUES(%s,%s,%s,"open",NOW())',
                (uid, subject, message)
            )
        except Exception as e:
            if '1146' in str(e):
                return None  # table doesn't exist yet
            raise

    # ── Public contact form (no login required) ────────────────────────────
    @classmethod
    def create_guest(cls, full_name, email, subject, message):
        body = f"From: {full_name} <{email}>\n\n{message}"
        try:
            return cls.execute(
                'INSERT INTO support_messages(user_id,subject,message,status,created_at) '
                'VALUES(0,%s,%s,"open",NOW())',
                (subject, body)
            )
        except Exception as e:
            if '1146' in str(e):
                return None
            raise

    # ── Get messages for one user ───────────────────────────────────────────
    @classmethod
    def get_for_user(cls, uid):
        try:
            return cls.fetch_all(
                'SELECT * FROM support_messages WHERE user_id=%s ORDER BY created_at DESC',
                (uid,)
            ) or []
        except Exception as e:
            if '1146' in str(e):
                return []
            raise

    # ── Get ALL messages (admin view) ───────────────────────────────────────
    @classmethod
    def all_messages(cls, status=None):
        try:
            base = (
                'SELECT sm.*, '
                'COALESCE(u.full_name, "Guest") AS full_name, '
                'COALESCE(u.email, "") AS email '
                'FROM support_messages sm '
                'LEFT JOIN users u ON u.id = sm.user_id AND sm.user_id != 0 '
            )
            if status:
                return cls.fetch_all(base + 'WHERE sm.status=%s ORDER BY sm.created_at DESC', (status,)) or []
            return cls.fetch_all(base + 'ORDER BY sm.created_at DESC') or []
        except Exception as e:
            if '1146' in str(e):
                return []
            raise

    # ── Get single message ──────────────────────────────────────────────────
    @classmethod
    def get_one(cls, mid):
        try:
            return cls.fetch_one(
                'SELECT sm.*, '
                'COALESCE(u.full_name, "Guest") AS full_name, '
                'COALESCE(u.email, "") AS email '
                'FROM support_messages sm '
                'LEFT JOIN users u ON u.id = sm.user_id AND sm.user_id != 0 '
                'WHERE sm.id=%s',
                (mid,)
            )
        except Exception:
            return None

    # ── Admin replies to a message ──────────────────────────────────────────
    @classmethod
    def reply(cls, mid, reply_text):
        return cls.execute(
            'UPDATE support_messages SET admin_reply=%s, status="replied", replied_at=NOW() WHERE id=%s',
            (reply_text, mid)
        )

    # ── Close a message ─────────────────────────────────────────────────────
    @classmethod
    def close(cls, mid):
        return cls.execute(
            'UPDATE support_messages SET status="closed" WHERE id=%s', (mid,)
        )

    # ── Count open/unread messages ──────────────────────────────────────────
    @classmethod
    def unread_count(cls):
        try:
            row = cls.fetch_one(
                "SELECT COUNT(*) AS cnt FROM support_messages WHERE status='open'"
            )
            return int(row['cnt']) if row else 0
        except Exception:
            return 0
