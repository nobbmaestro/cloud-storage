"""Test FileHandler class."""

import os
import shutil

import pytest
from werkzeug.datastructures import FileStorage

from cloud_storage.storage import (FileAlreadyExists, FileHandler,
                                   FileNotAllowed)


@pytest.fixture(scope="function")
def setup_and_teardown(storage_path, mock_fm):
    """Specific setup and teardown for the test cases."""
    shutil.rmtree(storage_path)
    os.mkdir(storage_path)
    whitelist = mock_fm.whitelist

    yield

    shutil.rmtree(storage_path)
    os.mkdir(storage_path)
    mock_fm.whitelist = whitelist


@pytest.mark.usefixtures("setup_and_teardown")
class TestFileHandler:
    """Collection of test suits for FileHandler."""

    _dummy_username = "foo_barsson"

    def test_create_user_area(self, mock_fm: FileHandler, paths):
        """Verifies `create_user_area` method."""
        # Ensure we are working from clean path
        path = paths["storage"] + "/" + self._dummy_username
        assert not self._helper_check_path_exists(path)

        # Create user storage area and verify
        assert mock_fm.create_user_area(self._dummy_username)
        assert self._helper_check_path_exists(path)

    def test_update_file_success(self, mock_fm: FileHandler, paths, file):
        """Verifies `upload_file` method."""
        # Create user storage area
        self._helper_create_user_path(paths)

        # Ensure we are working from clean path
        path = paths["storage"] + "/" + self._dummy_username + "/" + file.name
        assert not self._helper_check_path_exists(path)

        # Upload file and verify
        assert mock_fm.upload_file(self._dummy_username, file.name, file)
        assert self._helper_check_path_exists(path)

        # FileHandler shall raise FileAlreadyExists if we try to upload the same file again
        with pytest.raises(FileAlreadyExists):
            assert not mock_fm.upload_file(self._dummy_username, file.name, file)

    def test_update_file_failed(self, mock_fm: FileHandler, paths, file):
        """Verifies `upload_file` method."""
        # Create user storage area
        self._helper_create_user_path(paths)

        # Ensure we are working from clean path
        path = paths["storage"] + "/" + self._dummy_username + "/" + file.name
        assert not self._helper_check_path_exists(path)

        # Purge the white list
        mock_fm.whitelist = () 

        # FileHandler shall raise FileNotAllowed, due to file extension not being white listed
        with pytest.raises(FileNotAllowed):
            assert not mock_fm.upload_file(self._dummy_username, file.name, file)

        assert not self._helper_check_path_exists(path)

    def test_delete_file(self, mock_fm: FileHandler, paths, file):
        """Verifies `delete_file` method."""
        # Create user storage area
        self._helper_create_user_path(paths)
        assert self._helper_upload_file(paths["storage"], file)

        path = paths["storage"] + "/" + self._dummy_username + "/" + file.name

        # Delete file and verify
        assert mock_fm.delete_file(self._dummy_username, file.name)
        assert not self._helper_check_path_exists(path)

    def test_check_file_exists(self, mock_fm: FileHandler, paths, file):
        """Verifies `check_file_exists` method."""
        # Create user storage area
        self._helper_create_user_path(paths)

        path = paths["storage"] + "/" + self._dummy_username + "/" + file.name

        # Verify method when no file exists
        assert not self._helper_check_path_exists(path)
        assert not mock_fm.check_file_exists(self._dummy_username, file.name)

        # Add a file
        assert self._helper_upload_file(paths["storage"], file)

        # Verify method when file exists
        assert self._helper_check_path_exists(path)
        assert mock_fm.check_file_exists(self._dummy_username, file.name)

    @pytest.mark.skip(reason="Test not implemented")
    def test_get_file_size(self, mock_fm: FileHandler, paths, file):
        """Verifies `get_file_size` method."""
        assert False

    @pytest.mark.skip(reason="Test not implemented")
    def test_get_file_type(self, mock_fm: FileHandler, paths, file):
        """Verifies `get_file_type` method."""
        assert False

    @pytest.mark.skip(reason="Test not implemented")
    def test_get_file_path(self, mock_fm: FileHandler, paths, file):
        """Verifies `get_file_path` method."""
        assert False

    def _helper_check_path_exists(self, path) -> bool:
        """Check path exists helper."""
        return os.path.exists(path)

    def _helper_create_user_path(self, paths: dict) -> bool:
        """Create user path helper."""
        path = paths["storage"] + "/" + self._dummy_username
        if not self._helper_check_path_exists(path):
            os.mkdir(path)
        return self._helper_check_path_exists(path)

    def _helper_upload_file(self, root: str, file: FileStorage, username=None) -> bool:
        """Upload file to user storage area helper."""
        if not username:
            username = self._dummy_username

        path = root + "/" + username + "/" + str(file.name)
        if not self._helper_check_path_exists(path):
            file.save(path)

        return self._helper_check_path_exists(path)
