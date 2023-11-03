"""Database Exceptions."""


class UserAlreadyExists(Exception):
    """Raised when given `user_name` already exists in the database."""
