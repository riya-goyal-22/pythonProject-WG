import sqlite3
from typing import Tuple

class SQLiteQueryExecutor:
    @staticmethod
    def execute_query(conn: sqlite3.Connection, query: str, params: Tuple = ()) -> sqlite3.Cursor:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor