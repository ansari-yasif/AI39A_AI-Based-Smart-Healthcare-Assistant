"""app/models/medicine.py — Medicine reminders | Feature: Medicine Checker"""
from app.models.base_model import BaseModel


class MedicineModel(BaseModel):
    TABLE = 'medicines'

    @classmethod
    def add(cls, uid, name, dosage, times, frequency, start_date, end_date, notes):
        try:
            return cls.execute(
                'INSERT INTO medicines(user_id,name,dosage,times,frequency,start_date,end_date,notes,active,created_at) '
                'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,1,NOW())',
                (uid, name, dosage, times, frequency, start_date or None, end_date or None, notes)
            )
        except Exception as e:
            if 'active' in str(e):
                # Fallback if active column is missing
                return cls.execute(
                    'INSERT INTO medicines(user_id,name,dosage,times,frequency,start_date,end_date,notes,created_at) '
                    'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,NOW())',
                    (uid, name, dosage, times, frequency, start_date or None, end_date or None, notes)
                )
            raise

    @classmethod
    def get_for_user(cls, uid, active_only=True):
        res = []
        if active_only:
            try:
                res = cls.fetch_all(
                    'SELECT * FROM medicines WHERE user_id=%s AND active=1 ORDER BY created_at DESC', (uid,)
                )
            except Exception as e:
                # Fallback if 'active' column is missing (MySQL error 1054)
                if 'active' in str(e):
                    res = cls.fetch_all(
                        'SELECT * FROM medicines WHERE user_id=%s ORDER BY created_at DESC', (uid,)
                    )
                else:
                    raise
        else:
            res = cls.fetch_all(
                'SELECT * FROM medicines WHERE user_id=%s ORDER BY created_at DESC', (uid,)
            )
        
        # Ensure 'times' key exists to prevent template crashes if the column was missing
        for r in res:
            if 'times' not in r: r['times'] = ''
        return res

    @classmethod
    def get_one(cls, mid, uid):
        return cls.fetch_one('SELECT * FROM medicines WHERE id=%s AND user_id=%s', (mid, uid))

    @classmethod
    def deactivate(cls, mid, uid):
        return cls.execute('UPDATE medicines SET active=0 WHERE id=%s AND user_id=%s', (mid, uid))

    @classmethod
    def delete(cls, mid, uid):
        return cls.execute('DELETE FROM medicines WHERE id=%s AND user_id=%s', (mid, uid))

    @classmethod
    def log_dose(cls, mid, uid, log_date, scheduled_time, status='taken'):
        return cls.execute(
            'INSERT INTO medicine_logs(medicine_id,user_id,log_date,scheduled_time,status,taken_at) '
            'VALUES(%s,%s,%s,%s,%s,NOW())',
            (mid, uid, log_date, scheduled_time, status)
        )

    @classmethod
    def today_log(cls, uid, log_date):
        try:
            return cls.fetch_all(
                'SELECT * FROM medicine_logs WHERE user_id=%s AND log_date=%s', (uid, log_date)
            )
        except Exception as e:
            if '1146' in str(e): return []
            raise

    @classmethod
    def recent_logs(cls, uid, limit=30):
        try:
            return cls.fetch_all(
                'SELECT ml.*, m.name FROM medicine_logs ml '
                'JOIN medicines m ON m.id = ml.medicine_id '
                'WHERE ml.user_id=%s ORDER BY ml.taken_at DESC LIMIT %s',
                (uid, limit)
            )
        except Exception as e:
            if '1146' in str(e): return []
            raise

    @classmethod
    def adherence_rate(cls, uid, days=7):
        """Percentage of scheduled doses marked taken in the last N days."""
        try:
            row = cls.fetch_one(
                "SELECT COUNT(*) AS taken FROM medicine_logs "
                "WHERE user_id=%s AND status='taken' AND log_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)",
                (uid, days)
            )
            taken = int(row['taken']) if row else 0
        except Exception as e:
            if '1146' in str(e):
                taken = 0
            else:
                raise

        meds = cls.get_for_user(uid)
        if not meds:
            return 0
        expected = sum(len((m.get('times') or '').split(',')) for m in meds) * days
        if expected == 0:
            return 0
        return round(min(taken / expected, 1.0) * 100, 1)
