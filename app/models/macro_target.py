"""app/models/macro_target.py — Macro targets per day"""
from app.models.base_model import BaseModel


class MacroTargetModel(BaseModel):
    TABLE = 'macro_targets'

    @classmethod
    def get(cls, uid, target_date):
        return cls.fetch_one(
            'SELECT * FROM macro_targets WHERE user_id=%s AND target_date=%s',
            (uid, target_date)
        )

    @classmethod
    def save(cls, uid, target_date, protein, carbs, fat, calories):
        return cls.execute(
            'INSERT INTO macro_targets(user_id,target_date,protein_target,carbs_target,fat_target,calorie_target) '
            'VALUES(%s,%s,%s,%s,%s,%s) '
            'ON DUPLICATE KEY UPDATE protein_target=%s,carbs_target=%s,fat_target=%s,calorie_target=%s,updated_at=NOW()',
            (uid, target_date, protein, carbs, fat, calories,
             protein, carbs, fat, calories)
        )

    @classmethod
    def history(cls, uid, limit=30):
        return cls.fetch_all(
            'SELECT * FROM macro_targets WHERE user_id=%s ORDER BY target_date DESC LIMIT %s',
            (uid, limit)
        )
