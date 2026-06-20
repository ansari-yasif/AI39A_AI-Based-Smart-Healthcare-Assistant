"""app/database.py — MySQL DictCursor singleton wrapper"""
import pymysql
import pymysql.cursors
from flask import current_app, g
from typing import Any, Dict, List, Optional, Tuple


class Database:
    """Centralized DB access — all queries parameterized (no SQL injection)."""

    def _conn(self):
        if 'db_conn' not in g:
            g.db_conn = pymysql.connect(
                host=current_app.config['DB_HOST'],
                port=current_app.config['DB_PORT'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                db=current_app.config['DB_NAME'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False,
            )
        return g.db_conn

    def execute(self, sql: str, params: Tuple = ()) -> int:
        """INSERT / UPDATE / DELETE — returns lastrowid."""
        conn = self._conn()
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            conn.commit()
            return cur.lastrowid
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f'DB.execute error: {e}')
            raise
        finally:
            cur.close()

    def fetch_one(self, sql: str, params: Tuple = ()) -> Optional[Dict]:
        """SELECT single row → dict or None."""
        conn = self._conn()
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            return cur.fetchone()
        finally:
            cur.close()

    def fetch_all(self, sql: str, params: Tuple = ()) -> List[Dict]:
        """SELECT multiple rows → list of dicts."""
        conn = self._conn()
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            return cur.fetchall()
        finally:
            cur.close()

    def transaction(self, queries: List[Tuple[str, Tuple]]) -> bool:
        """Run multiple queries atomically."""
        conn = self._conn()
        cur = conn.cursor()
        try:
            for sql, params in queries:
                cur.execute(sql, params)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f'DB.transaction rollback: {e}')
            return False
        finally:
            cur.close()

    def close(self):
        conn = g.pop('db_conn', None)
        if conn:
            conn.close()


db = Database()


def close_db(error=None):
    """Teardown — called automatically after each request."""
    db.close()
