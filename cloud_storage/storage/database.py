"""Database Class."""

import datetime
import sqlite3
from typing import Callable

from .exceptions import UserAlreadyExists, UserNotFound
from .strategies import PasswordHashManager, dict_factory


class Database:
    """Implements database class."""

    def __init__(
        self,
        database_name,
        hash_strategy: Callable = PasswordHashManager,
        row_strategy: Callable = dict_factory,
    ):
        self._conn = sqlite3.connect(
            database_name,
            check_same_thread=False,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        self._conn.row_factory = row_strategy
        self._cursor = self._conn.cursor()
        self._hash_stragegy = hash_strategy()

    def _execute_query(self, query, params: list = []):
        """Execute query."""
        if params:
            self._cursor.execute(query, params)
        else:
            self._cursor.execute(query)

        return self._cursor.fetchall()

    def _commit(self):
        """Commit changes to database."""
        self._conn.commit()

    def _close(self):
        """Close database connection."""
        self._conn.close()

    def add_user(self, user_name: str, password: str) -> bool:
        """Add user to the database."""
        success = False
        # Check whether username already exists, insert to database if no matches exists
        if not self.check_user_exists(user_name):
            # Create password hash
            hash = self._hash_stragegy.generate_hash(password)

            # Insert user into the database
            self._execute_query("INSERT INTO users (user_name, password) VALUES(?, ?)", [user_name, hash])
            self._commit()
            success = self.check_user_exists(user_name)

        else:
            raise UserAlreadyExists("user `%s` already exists" % user_name)

        return success

    def upload_file(self, user_id: int, file_name: str, file_size: float, file_type: str) -> bool:
        """Upload the associated meta data of a given file to the database."""
        timestamp = datetime.datetime.now(datetime.UTC)
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

    def delete_file(self, user_id: int, file_name: str) -> bool:
        """Delete `file_name` associated with the user."""
        query = "DELETE FROM files WHERE user_id = ? AND file_name = ?"

        success = False
        # Check whether file_name exists
        if self.check_file_exists(user_id, file_name):
            self._execute_query(query, [user_id, file_name])
            self._commit()

            success = not self.check_file_exists(user_id, file_name)

        return success

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
        if len(rows) == 1 and self._hash_stragegy.check_password(rows[0]["password"], password):
            match = True

        return match

    def check_file_exists(self, user_id: int, file_name: str) -> bool:
        """Search for `file_name` associated with `user_id` in the database."""
        exists = False
        query = "SELECT file_name FROM files WHERE user_id = ? AND file_name = ?"

        if len(self._execute_query(query, [user_id, file_name])):
            exists = True

        return exists

    def get_list_of_files(self, user_id: int, order_by: str = "file_name", ascending: bool = True) -> list:
        """Get list of files for a given `user_id`."""
        query = "SELECT * FROM files WHERE user_id = ? ORDER BY #1 #2"

        # Verify and assign column name given by the user
        if order_by in ["file_name", "type", "modified", "size"]:
            query = query.replace("#1", order_by)
        else:
            query = query.replace("#1", "file_name")

        # Assign order direction
        if ascending:
            query = query.replace("#2", "ASC")
        else:
            query = query.replace("#2", "DESC")

        try:
            files = self._execute_query(query, [user_id])

        except sqlite3.InternalError:
            files = []

        return files

    def get_user_id(self, user_name: str) -> int:
        """Get user_id by `user_name`."""
        query = "SELECT id FROM users WHERE user_name = ?"
        result = self._execute_query(query, [user_name])

        # Raise fault if user not found
        if len(result) == 0:
            raise UserNotFound("username `%s` does not exist" % user_name)

        else:
            user_id = int(result[0]["id"])

        return user_id

    def get_username_by_id(self, user_id: int) -> str:
        """Get user_name by `user_id`."""
        query = "SELECT user_name FROM users WHERE id = ?"
        result = self._execute_query(query, [user_id])

        # Raise fault if user not found
        if len(result) == 0:
            raise UserNotFound("user_id `%d` does not exist" % user_id)

        else:
            user_name = result[0]["user_name"]

        return user_name

    def search_file(self, user_id: int, file_name: str, strict_beg: bool = False, strict_end: bool = False) -> list:
        """Search for `file_name` pattern in users database."""
        query = """
            SELECT
                file_name, file_type, created_at, updated_at, file_size
            FROM
                files
            WHERE
                user_id = ? AND file_name LIKE ?
            ORDER BY
                file_name ASC
        """
        if not strict_beg and not strict_end:
            pattern = "%%%s%%" % file_name
        elif not strict_beg:
            pattern = "%%%s" % file_name
        elif not strict_end:
            pattern = "%s%%" % file_name
        else:
            pattern = "%s" % file_name

        return self._execute_query(query, [user_id, pattern])
