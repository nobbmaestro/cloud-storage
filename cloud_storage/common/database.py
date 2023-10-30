"""Database Class."""

import sqlite3
from datetime import datetime
from typing import Callable

from werkzeug.security import check_password_hash, generate_password_hash


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

    def _execute_query(self, query, params: list = []):
        """Execute query."""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return self.cursor.fetchall()

    def _commit(self):
        """Commit changes to database."""
        self.conn.commit()

    def _close(self):
        """Close database connection."""
        self.conn.close()

    def check_user_exists(self, user_name: str) -> bool:
        """Check if `user_name` exists in database."""
        query = "SELECT user_name FROM users WHERE user_name = ?"
        return True if self._execute_query(query, [user_name]) else False

    def check_user_credentials(self, user_name: str, password: str) -> bool:
        """Check user cridentials."""
        match = False

        # Query database for username
        rows = self._execute_query("SELECT * FROM users WHERE user_name = ?", [user_name])

        # Ensure username exists and password is correct
        if len(rows) == 1 and check_password_hash(rows[0]["hash"], password):
            match = True

        return match

    def add_user(self, user_name: str, password: str) -> bool:
        """Add user to the database."""
        success = False
        # Check whether username already exists, insert to database if no matches exists
        if not self.check_user_exists(user_name):
            # Create password hash
            hash = generate_password_hash(password)

            # Insert user into the database
            self._execute_query("INSERT INTO users (user_name, hash) VALUES(?, ?)", [user_name, hash])
            self._commit()
            success = self.check_user_exists(user_name)

        return success

    def upload_file(self, user_id: int, file_name: str, file_size: float, file_type: str) -> bool:
        """Upload the associated meta data of a given file to the database."""
        timestamp = datetime.now()
        params = [file_name, file_type, file_size, user_id, timestamp, 0]
        query = "INSERT INTO files (file_name, file_type, file_size, user_id, created_at, revision) VALUES (?, ?, ?, ?, ?, ?)"

        # TODO: Subtract file_size from users available storage

        try:
            self._execute_query(query, params)
            self._commit()
            success = True

        except sqlite3.InternalError:
            success = False

        return success

    def update_file(self):
        raise NotImplemented

    def get_files(self, user_id: int) -> list:
        query = "SELECT * FROM files WHERE user_id = ?"

        try:
            files = self._execute_query(query, [user_id])

        except sqlite3.InternalError:
            files = []

        return files

    def get_user_id(self, user_name: str) -> str:
        """Get user_id by `user_name`."""
        query = "SELECT id FROM users WHERE user_name = ?"
        return self._execute_query(query, [user_name])[0]["id"]

    def get_username_by_id(self, user_id: int) -> str:
        """Get user_name by `user_id`."""
        query = "SELECT user_name FROM users WHERE id = ?"

        res = self._execute_query(query, [user_id])
        if "user_name" in res[0]:
            user_name = res[0]["user_name"]
        else:
            user_name = ""

        return user_name

    def check_file_exists(self, user_id: int, file_name: str) -> bool:
        """Search for `file_name` associated with `user_id` in the database."""
        exists = False
        query = "SELECT file_name FROM files WHERE user_id = ? AND file_name = ?"

        if len(self._execute_query(query, [user_id, file_name])):
            exists = True

        return exists
