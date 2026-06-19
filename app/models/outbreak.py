"""app/models/outbreak.py — Outbreak alerts | Feature: Outbreak Alerts"""
from app.models.base_model import BaseModel


class OutbreakModel(BaseModel):
    TABLE = 'outbreak_alerts'

    @classmethod
    def active_alerts(cls):
        try:
            return cls.fetch_all(
                "SELECT * FROM outbreak_alerts WHERE active=1 "
                "AND (expires_at IS NULL OR expires_at > NOW()) "
                "ORDER BY severity DESC, created_at DESC"
            )
        except Exception as e:
            # If table doesn't exist (MySQL error 1146), return empty list instead of crashing
            if '1146' in str(e):
                return []
            raise

    @classmethod
    def all_alerts(cls):
        try:
            return cls.fetch_all('SELECT * FROM outbreak_alerts ORDER BY created_at DESC')
        except Exception as e:
            if '1146' in str(e):
                return []
            raise

    @classmethod
    def create(cls, title, description, severity, region, expires_at=None):
        return cls.execute(
            'INSERT INTO outbreak_alerts(title,description,severity,region,active,created_at,expires_at) '
            'VALUES(%s,%s,%s,%s,1,NOW(),%s)',
            (title, description, severity, region, expires_at or None)
        )

    @classmethod
    def deactivate(cls, aid):
        return cls.execute('UPDATE outbreak_alerts SET active=0 WHERE id=%s', (aid,))

    @classmethod
    def delete(cls, aid):
        return cls.execute('DELETE FROM outbreak_alerts WHERE id=%s', (aid,))
