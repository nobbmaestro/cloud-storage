"""Database Class."""

import sqlite3
from datetime import datetime
from os.path import exists
from typing import Callable, List, Optional


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database:
    """Implements database class."""

    def __init__(self, database_name, strategy: Callable = dict_factory):
        self.conn = sqlite3.connect(database_name, check_same_thread=False)
        self.conn.row_factory = strategy
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params: Optional[List[str]] = None):
        """Execute query."""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return self.cursor.fetchall()

    def upload_file(self, user_id: int, file_name: str, file_size: float, file_type: str) -> bool:
        timestamp = datetime.now()
        params = [file_name, file_type, file_size, user_id, timestamp, 0]
        query = "INSERT INTO files (file_name, file_type, file_size, user_id, created_at, revision) VALUES (?, ?, ?, ?, ?, ?)"

        # TODO: Subtract file_size from users available storage

        try:
            self.execute_query(query, params)
            self.commit()
            success = True

        except sqlite3.InternalError:
            success = False

        return success

    def update_file(self):
        raise NotImplemented

    def get_files(self, user_id: int) -> list:
        query = "SELECT * FROM files WHERE user_id = ?"

        try:
            files = self.execute_query(query, [user_id])

        except sqlite3.InternalError:
            files = []

        return files

    def commit(self):
        """Commit changes to database."""
        self.conn.commit()

    def close(self):
        """Close database connection."""
        self.conn.close()

    def get_username_by_id(self, user_id: int) -> str:
        """Get user_name by `user_id`."""
        query = "SELECT user_name FROM users WHERE id = ?"

        res = self.execute_query(query, [user_id])
        if "user_name" in res[0]:
            user_name = res[0]["user_name"]
        else:
            user_name = ""

        return user_name

    def check_file_exists(self, user_id: int, file_name: str) -> bool:
        """Search for `file_name` associated with `user_id` in the database."""
        exists = False
        query = "SELECT file_name FROM files WHERE user_id = ? AND file_name = ?"

        if len(self.execute_query(query, [user_id, file_name])):
            exists = True

        return exists
