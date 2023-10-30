"""StorageHandler class."""

import logging
from typing import Any

from flask import Flask
from werkzeug.utils import secure_filename

from cloud_storage.common import Database, FileHandler
from cloud_storage.common.file_handler import FileNotAllowed

logger = logging.getLogger(__name__)


class StorageHandler:
    """Implements StorageHandler class."""

    def __init__(self, app: Flask, db: Database, fm: FileHandler):
        self._app = app
        self._db = db
        self._fm = fm

    def upload_file(self, user_id: int, file: Any) -> bool:
        """Upload `file` to users cloud storage area."""
        user_name = self._db.get_username_by_id(user_id)

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

    def get_file(self, user: str, file_name: str) -> Any:
        raise NotImplemented

    def _get_secure_filename(self, file_name: str) -> str:
        """Getter for secure version of `file_name`."""
        return secure_filename(file_name)

    def check_file_exists(self, user_id: int, file_name: str) -> bool:
        """Search `user` storage for `file_name`."""
        return self._db.check_file_exists(user_id, file_name)
