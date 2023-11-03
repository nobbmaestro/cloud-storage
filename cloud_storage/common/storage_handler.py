"""StorageHandler class."""

import logging
from typing import Any

from flask import Flask
from werkzeug.utils import secure_filename

from cloud_storage.common import FileHandler
from cloud_storage.common.file_handler import FileNotAllowed
from cloud_storage.database import Database

logger = logging.getLogger(__name__)


class StorageHandler:
    """Implements StorageHandler class."""

    def __init__(self, app: Flask, db: Database, fm: FileHandler):
        self._app = app
        self._db = db
        self._fm = fm

    def add_user(self, user_name: str, password: str) -> bool:
        """Add user."""
        success = self._db.add_user(user_name, password)
        success &= self._fm.create_user_area(user_name)

        return success

    def upload_file(self, user_id: int, files: List[Any]) -> bool:
        """Upload `file`(s) to user cloud storage area."""
        user_name = self._db.get_username_by_id(user_id)
    
        success = False
        if isinstance(files, list):
            for file in files:
                success = self._upload_file(user_id, user_name, file) 
                if not success:
                    break

        elif isinstance(files, str):
            success = self._upload_file(user_id, user_name, files)

        return success

    def _upload_file(self, user_id: int, user_name: str, file: Any) -> bool:
        """Upload `file` to user cloud storage area."""

        # Collect file meta data
        file_name = self._get_secure_filename(file.filename)
        file_type = self._fm.get_file_type(file_name)

        success = False
        if not self.check_file_exists(user_id, file_name):
            try:
                success = self._fm.upload_file(user_name, file_name, file)
                # File is saved to the drive, check the size
                file_size = self._fm.get_file_size(user_name, file_name)
                success &= self._db.upload_file(user_id, file_name, file_size, file_type)

            except FileNotAllowed:
                logger.warning("file not allowed")

        return success

    def remove_file(self, user_id: int, file_name) -> bool:
        """Remove `file_name` from the users cloud storage."""
        user_name = self._db.get_username_by_id(user_id)

        success = self._db.remove_file(user_id, file_name)
        success &= self._fm.remove_file(user_name, file_name)

        return success

    def get_file_path(self, user_id: int, file_name: str) -> str:
        path = ""
        if self.check_file_exists(user_id, file_name):
            user_name = self._db.get_username_by_id(user_id)
            path = self._fm.get_file_path(user_name, file_name)

        return path

    def _get_secure_filename(self, file_name: str) -> str:
        """Getter for secure version of `file_name`."""
        return secure_filename(file_name)

    def check_file_exists(self, user_id: int, file_name: str) -> bool:
        """Search `user` storage for `file_name`."""
        return self._db.check_file_exists(user_id, file_name)

    def search_file(self, user_id: int, file_name: str) -> list:
        """Search for `file_name` pattern in the users clourd storage."""
        return self._db.search_file(user_id, file_name)
