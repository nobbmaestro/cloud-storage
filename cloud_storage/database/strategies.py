"""Database Strategies."""

from werkzeug.security import check_password_hash, generate_password_hash


def dict_factory(cursor, row) -> dict:
    """SQLite3 row to dict factory."""
    row_dict = {}
    for idx, col in enumerate(cursor.description):
        row_dict[col[0]] = row[idx]
    return row_dict


class PasswordHashManager:
    """Implements password hash strategy class."""

    _method = "scrypt"
    _salt_length = 16

    def generate_hash(self, password: str) -> str:
        """Generate password hash."""
        return generate_password_hash(password, self._method, self._salt_length)

    def check_password(self, hash: str, password: str) -> bool:
        """Check hash matches the password."""
        return check_password_hash(hash, password)
