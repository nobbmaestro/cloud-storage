"""Database Class."""

import sqlite3
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

    def commit(self):
        """Commit changes to database."""
        self.conn.commit()

    def close(self):
        """Close database connection."""
        self.conn.close()
