"""Database Exceptions."""


class FileAlreadyExists(Exception):
    """Raised when given `file_name` already exists in the storage."""


class FileNotAllowed(Exception):
    """Raised when non-whitelisted file extension is given."""


class UserAlreadyExists(Exception):
    """Raised when given `user_name` already exists in the database."""


class UserNotFound(Exception):
    """Raised when given `user_name` does not exist in the database."""
