"""Database Exceptions."""


class FileNotAllowed(Exception):
    """Raised when non-whitelisted file extension is given."""


class UserAlreadyExists(Exception):
    """Raised when given `user_name` already exists in the database."""


class UserNotFound(Exception):
    """Raised when given `user_name` does not exist in the database."""
