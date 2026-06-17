"""app/models/bmi.py — BMI records persistent model"""
from app.models.base_model import BaseModel


class BMIModel(BaseModel):
    TABLE = 'bmi_records'

    @classmethod
    def _ensure_schema(cls):
        """Add bmi_color column if it doesn't exist (migration safety)."""
        try:
            cls.execute(
                "ALTER TABLE bmi_records ADD COLUMN IF NOT EXISTS bmi_color VARCHAR(20) DEFAULT '#22c55e'"
            )
        except Exception:
            pass

    @classmethod
    def save(cls, uid, weight_kg, height_cm, bmi_value, bmi_label, bmi_color):
        # Try with bmi_color; fall back if column missing
        try:
            return cls.execute(
                'INSERT INTO bmi_records(user_id,weight_kg,height_cm,bmi_value,bmi_label,bmi_color,recorded_at,created_at) '
                'VALUES(%s,%s,%s,%s,%s,%s,CURDATE(),NOW())',
                (uid, weight_kg, height_cm, bmi_value, bmi_label, bmi_color)
            )
        except Exception as e:
            if 'bmi_color' in str(e):
                # Column doesn't exist yet — run migration then retry
                try:
                    cls.execute(
                        "ALTER TABLE bmi_records ADD COLUMN bmi_color VARCHAR(20) DEFAULT '#22c55e'"
                    )
                except Exception:
                    pass
                return cls.execute(
                    'INSERT INTO bmi_records(user_id,weight_kg,height_cm,bmi_value,bmi_label,recorded_at,created_at) '
                    'VALUES(%s,%s,%s,%s,%s,CURDATE(),NOW())',
                    (uid, weight_kg, height_cm, bmi_value, bmi_label)
                )
            raise

    @classmethod
    def history(cls, uid, limit=10):
        return cls.fetch_all(
            'SELECT * FROM bmi_records WHERE user_id=%s ORDER BY recorded_at DESC, id DESC LIMIT %s',
            (uid, limit)
        )

    @classmethod
    def latest(cls, uid):
        return cls.fetch_one(
            'SELECT * FROM bmi_records WHERE user_id=%s ORDER BY recorded_at DESC, id DESC LIMIT 1',
            (uid,)
        )
