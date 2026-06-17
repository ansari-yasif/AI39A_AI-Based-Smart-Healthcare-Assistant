"""app/models/support.py — Support messages to admin | Feature: Contact Admin"""
from app.models.base_model import BaseModel


class SupportModel(BaseModel):
    TABLE = 'support_messages'

    @classmethod
    def create(cls, uid, subject, message):
        try:
            return cls.execute(
                'INSERT INTO support_messages(user_id,subject,message,status,created_at) '
                'VALUES(%s,%s,%s,"open",NOW())',
                (uid, subject, message)
            )
        except Exception as e:
            if '1146' in str(e): return None
            raise

    @classmethod
    def get_for_user(cls, uid):
        try:
            return cls.fetch_all(
                'SELECT * FROM support_messages WHERE user_id=%s ORDER BY created_at DESC', (uid,)
            )
        except Exception as e:
            if '1146' in str(e): return []
            raise

    @classmethod
    def all_messages(cls, status=None):
        try:
            if status:
                return cls.fetch_all(
                    'SELECT sm.*, u.full_name, u.email FROM support_messages sm '
                    'JOIN users u ON u.id = sm.user_id '
                    'WHERE sm.status=%s ORDER BY sm.created_at DESC', (status,)
                )
            return cls.fetch_all(
                'SELECT sm.*, u.full_name, u.email FROM support_messages sm '
                'JOIN users u ON u.id = sm.user_id '
                'ORDER BY sm.created_at DESC'
            )
        except Exception as e:
            if '1146' in str(e): return []
            raise

    @classmethod
    def get_one(cls, mid):
        return cls.fetch_one(
            'SELECT sm.*, u.full_name, u.email FROM support_messages sm '
            'JOIN users u ON u.id = sm.user_id WHERE sm.id=%s', (mid,)
        )

    @classmethod
    def reply(cls, mid, reply_text):
        return cls.execute(
            'UPDATE support_messages SET admin_reply=%s, status="replied", replied_at=NOW() WHERE id=%s',
            (reply_text, mid)
        )

    @classmethod
    def close(cls, mid):
        return cls.execute('UPDATE support_messages SET status="closed" WHERE id=%s', (mid,))

    @classmethod
    def unread_count(cls):
        try:
            row = cls.fetch_one("SELECT COUNT(*) AS cnt FROM support_messages WHERE status='open'")
            return int(row['cnt']) if row else 0
        except Exception as e:
            if '1146' in str(e): return 0
            raise
