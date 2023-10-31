"""FileHandler class."""

import logging
import os
from typing import Any

from flask import Flask

logger = logging.getLogger(__name__)

# TODO: Add support for file compression
#   read more: https://www.tutorialspoint.com/how-to-compress-files-with-zipfile-module-in-python


class FileNotAllowed(Exception):
    """Raised when non-whitelisted file extension is given."""

    pass


class FileHandler:
    """Implements FileHandler class."""

    _whitelist = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "mov"}

    def __init__(self, app: Flask, root: str) -> None:
        self._app = app
        self._root_path = root

    def create_user_area(self, user_name: str) -> bool:
        """Create `user_name` storage area.

        Return `True` if successful.
        """
        path = self.get_file_path(user_name)
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info("creating path: %s" % path)

        return os.path.exists(path)

    def upload_file(self, user_name: str, file_name: str, file: Any) -> bool:
        """Upload `file` to the `user_name` storage area."""
        success = False
        path = self.get_file_path(user_name, file_name)

        # Check if file extension exists in the whitelist
        if not self.check_file_extension(file_name):
            raise FileNotAllowed

        # Check if file already exists
        if not self.check_file_exists(user_name, file_name):
            logger.info("uploading file: %s" % file_name)
            file.save(path)

        else:
            self.update_file(user_name, file)

        success = self.check_file_exists(user_name, file_name)

        return success

    def update_file(self, user_name, file: Any) -> bool:
        """Update `file` on the `user_name` storage area."""
        return False

    def remove_file(self, user_name: str, file_name: str) -> bool:
        """Remove file from the user storage."""
        success = False
        if self.check_file_exists(user_name, file_name):
            path = self.get_file_path(user_name, file_name)
            os.remove(path)
            success = not self.check_file_exists(user_name, file_name)

        return success

    def check_file_exists(self, user_name: str, file_name: str) -> bool:
        """Check if file exists in the `user_name` storage area."""
        path = self.get_file_path(user_name, file_name)
        return os.path.exists(path)

    def get_file_size(self, user_name: str, file_name: str) -> float:
        """Get size of the file."""
        size = 0.0
        path = self.get_file_path(user_name, file_name)

        if self.check_file_exists(user_name, file_name):
            size = os.stat(path).st_size

        return size

    def get_file_type(self, file_name: str) -> str:
        """Get file type based on file extension."""
        return file_name.rsplit(".", 1)[1].lower()

    def get_file_path(self, user_name: str, file_name: str = "") -> str:
        """Get the absolute path to the file."""
        path = ""

        if user_name:
            path = self._root_path + "/" + user_name + "/" + file_name
        else:
            path = self._root_path + "/" + user_name + "/"

        return path

    def check_file_extension(self, file_name):
        """Check if file extension exists on the whitelist."""
        return "." in file_name and file_name.rsplit(".", 1)[1].lower() in self._whitelist
