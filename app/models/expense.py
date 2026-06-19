"""app/models/expense.py — Health expense tracking | Feature: Expense Tracker"""
from app.models.base_model import BaseModel


class ExpenseModel(BaseModel):
    TABLE = 'health_expenses'

    @classmethod
    def add(cls, uid, category, amount, description, expense_date):
        try:
            return cls.execute(
                'INSERT INTO health_expenses(user_id,category,amount,description,expense_date,created_at) '
                'VALUES(%s,%s,%s,%s,%s,NOW())',
                (uid, category, amount, description, expense_date)
            )
        except Exception as e:
            if '1146' in str(e):
                return None
            raise

    @classmethod
    def get_for_user(cls, uid, limit=100):
        try:
            return cls.fetch_all(
                'SELECT * FROM health_expenses WHERE user_id=%s ORDER BY expense_date DESC LIMIT %s',
                (uid, limit)
            )
        except Exception as e:
            if '1146' in str(e): return []
            raise

    @classmethod
    def delete(cls, eid, uid):
        return cls.execute('DELETE FROM health_expenses WHERE id=%s AND user_id=%s', (eid, uid))

    @classmethod
    def total_for_period(cls, uid, start, end):
        try:
            row = cls.fetch_one(
                'SELECT COALESCE(SUM(amount),0) AS total, COUNT(*) AS cnt '
                'FROM health_expenses WHERE user_id=%s AND expense_date BETWEEN %s AND %s',
                (uid, start, end)
            )
            return row or {'total': 0, 'cnt': 0}
        except Exception as e:
            if '1146' in str(e):
                return {'total': 0, 'cnt': 0}
            raise

    @classmethod
    def by_category(cls, uid, start, end):
        try:
            return cls.fetch_all(
                'SELECT category, COALESCE(SUM(amount),0) AS total, COUNT(*) AS cnt '
                'FROM health_expenses WHERE user_id=%s AND expense_date BETWEEN %s AND %s '
                'GROUP BY category ORDER BY total DESC',
                (uid, start, end)
            )
        except Exception as e:
            if '1146' in str(e): return []
            raise

    @classmethod
    def monthly_trend(cls, uid, months=6):
        try:
            return cls.fetch_all(
                "SELECT DATE_FORMAT(expense_date, '%%Y-%%m') AS ym, COALESCE(SUM(amount),0) AS total "
                "FROM health_expenses WHERE user_id=%s AND expense_date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH) "
                "GROUP BY ym ORDER BY ym ASC",
                (uid, months)
            )
        except Exception as e:
            if '1146' in str(e): return []
            raise
