"""Test Database class."""

import datetime
from typing import Any, List

import pytest

from cloud_storage.database import Database, UserAlreadyExists, UserNotFound
from cloud_storage.database.strategies import PasswordHashManager


@pytest.fixture(scope="function")
def setup_and_teardown(mock_db, sql_script):
    """Specific setup and teardown for the test cases."""
    # Ensure purges database
    mock_db._cursor.executescript(sql_script)

    yield

    # Clean up
    mock_db._cursor.executescript(sql_script)


class TestPasswordHashManager:
    """Collection of test suits for PasswordHashManager."""

    _test_obj = PasswordHashManager()

    @pytest.mark.parametrize(
        "value",
        [
            ("test"),
            ("password"),
            ("12345"),
        ],
    )
    def test_generate_hash(self, value):
        """Verifies `generate_hash` method."""
        # Verify unique hashes on identical passwords
        first_password = self._test_obj.generate_hash(value)
        second_password = self._test_obj.generate_hash(value)

        assert first_password is not second_password

    @pytest.mark.parametrize(
        "value",
        [
            ("test"),
            ("password"),
            ("12345"),
        ],
    )
    def test_check_password(self, value):
        """Verifies `check_password` method."""
        hash = self._test_obj.generate_hash(value)
        assert self._test_obj.check_password(hash, value)


@pytest.mark.usefixtures("setup_and_teardown")
class TestDatabase:
    """Collection of test suits for Database."""

    _dummy_username = "dummy_user"
    _dummy_password = "dummy_password"
    _dummy_user_id = 1

    _dummy_file_name = "foo.bar"
    _dummy_file_size = 123
    _dummy_file_type = "Foo Bar "

    def test_add_user(self, mock_db: Database):
        """Verifies `add_user` method."""
        # Replace default hash strategy with dummy
        mock_db._hash_stragegy = DummyPasswordHashManager()

        # Add the new user and obtain the results from the database
        self._helper_add_user(mock_db)
        result = mock_db._cursor.execute("SELECT * FROM users").fetchall()[0]

        # Verify that the newly added user exists
        assert result["user_name"] == self._dummy_username
        assert result["password"] == self._dummy_password

        # Try to add user again, UserAlreadyExists shall be raised
        with pytest.raises(UserAlreadyExists):
            mock_db.add_user(self._dummy_username, self._dummy_password)

    def test_check_user_exists(self, mock_db: Database):
        """Verifies `check_user_exists` method."""
        # User not added, thus, does not exist
        assert not mock_db.check_user_exists(self._dummy_username)
        self._helper_add_user(mock_db)
        assert mock_db.check_user_exists(self._dummy_username)

    def test_check_user_credentials(self, mock_db: Database):
        """Verifies `check_user_credentials` method."""
        self._helper_add_user(mock_db)
        assert mock_db.check_user_credentials(self._dummy_username, self._dummy_password)
        assert not mock_db.check_user_credentials(self._dummy_username, "password")

    def test_upload_file(self, mock_db: Database):
        """Verifies `upload_file` method."""
        # Verify that file does not exist
        assert not mock_db._cursor.execute(
            "SELECT * FROM files WHERE file_name = ?", [self._dummy_file_name]
        ).fetchall()

        # Add the file
        mock_db.upload_file(self._dummy_user_id, self._dummy_file_name, self._dummy_file_size, self._dummy_file_type)

        # Verify that file exists and meta data matches
        result = mock_db._cursor.execute("SELECT * FROM files WHERE file_name = ?", [self._dummy_file_name]).fetchall()
        assert result[0]["file_name"] == self._dummy_file_name
        assert result[0]["file_size"] == self._dummy_file_size
        assert result[0]["file_type"] == self._dummy_file_type
        assert result[0]["revision"] == 0
        assert result[0]["updated_at"] == None
        assert isinstance(result[0]["created_at"], datetime.datetime)

    @pytest.mark.skip(reason="Not implemented")
    def test_update_file(self, mock_db: Database):
        """Verifies `update_file` method."""
        assert False

    def test_delete_file(self, mock_db: Database):
        """Verifies `delete_file` method."""
        # Verify that file does not exist
        assert not mock_db._cursor.execute(
            "SELECT * FROM files WHERE file_name = ?", [self._dummy_file_name]
        ).fetchall()

        # Add the file
        mock_db.upload_file(self._dummy_user_id, self._dummy_file_name, self._dummy_file_size, self._dummy_file_type)
        assert mock_db._cursor.execute("SELECT * FROM files WHERE file_name = ?", [self._dummy_file_name]).fetchall()

        # Delete the file
        mock_db.delete_file(self._dummy_user_id, self._dummy_file_name)
        assert not mock_db._cursor.execute(
            "SELECT * FROM files WHERE file_name = ?", [self._dummy_file_name]
        ).fetchall()

    def test_get_list_of_files(self, mock_db: Database):
        """Verifies `get_list_of_files` method."""
        # No file in the database, method shall reflect that
        assert not self._helper_check_file_exists(mock_db)
        assert not mock_db.get_list_of_files(self._dummy_user_id)

        # Add a file and verify
        self._helper_add_file(mock_db)
        result = mock_db.get_list_of_files(self._dummy_user_id)

        assert len(result) == 1
        assert result[0]["file_name"] == self._dummy_file_name

    def test_get_user_id(self, mock_db: Database):
        """Verifies `get_user_id` method."""
        # User not yet added, shall raise UserNotFound
        with pytest.raises(UserNotFound):
            assert not mock_db.get_user_id(self._dummy_username)

        # Add user, method shall return user_id
        self._helper_add_user(mock_db)
        assert mock_db.get_user_id(self._dummy_username) == self._dummy_user_id

    def test_get_username_by_id(self, mock_db: Database):
        """Verifies `get_username_by_id` method."""
        # User not yet added, shall raise UserNotFound
        with pytest.raises(UserNotFound):
            assert not mock_db.get_username_by_id(self._dummy_user_id)

        # Add user, method shall return user_id
        self._helper_add_user(mock_db)
        assert mock_db.get_username_by_id(self._dummy_user_id) == self._dummy_username

    def test_check_file_exists(self, mock_db: Database):
        """Verifies `check_file_exists` method."""
        # Verify that file does not exist
        assert not self._helper_check_file_exists(mock_db)
        assert not mock_db.check_file_exists(self._dummy_user_id, self._dummy_file_name)

        # Add the file
        self._helper_add_file(mock_db)
        assert self._helper_check_file_exists(mock_db)
        assert mock_db.check_file_exists(self._dummy_user_id, self._dummy_file_name)

        # Delete the file
        self._helper_delete_file(mock_db)
        assert not self._helper_check_file_exists(mock_db)
        assert not mock_db.check_file_exists(self._dummy_user_id, self._dummy_file_name)

    @pytest.mark.parametrize(
        "pattern, expected",
        [
            ("foo", ["bar.foo", "foo.bar", "foo.foo"]),
            ("bar", ["bar.bar", "bar.foo", "foo.bar"]),
        ],
    )
    def test_search_file_base_case(self, mock_db: Database, pattern, expected):
        """Verifies `search_file` method."""
        # Add various files
        for file_name in ["foo.bar", "bar.foo", "foo.foo", "bar.bar"]:
            self._helper_add_file(mock_db, file_name)

        # Search for name pattern
        result = mock_db.search_file(self._dummy_user_id, pattern)

        assert self._helper_compare_list_to_dict(expected, result, "file_name")

    @pytest.mark.parametrize(
        "pattern, expected",
        [
            ("foo", ["bar.foo", "foo.foo"]),
            ("bar", ["bar.bar", "foo.bar"]),
        ],
    )
    def test_search_file_strict_end_case(self, mock_db: Database, pattern, expected):
        """Verifies `search_file` method."""
        # Add various files
        for file_name in ["foo.bar", "bar.foo", "foo.foo", "bar.bar"]:
            self._helper_add_file(mock_db, file_name)

        # Search for name ending pattern
        result = mock_db.search_file(self._dummy_user_id, pattern, strict_beg=False, strict_end=True)

        assert self._helper_compare_list_to_dict(expected, result, "file_name")

    @pytest.mark.parametrize(
        "pattern, expected",
        [
            ("foo", ["foo.bar", "foo.foo"]),
            ("bar", ["bar.bar", "bar.foo"]),
        ],
    )
    def test_search_file_strict_beg_case(self, mock_db: Database, pattern, expected):
        """Verifies `search_file` method."""
        # Add various files
        for file_name in ["foo.bar", "bar.foo", "foo.foo", "bar.bar"]:
            self._helper_add_file(mock_db, file_name)

        # Search for name begging pattern
        result = mock_db.search_file(self._dummy_user_id, pattern, strict_beg=True, strict_end=False)

        assert self._helper_compare_list_to_dict(expected, result, "file_name")

    @pytest.mark.parametrize(
        "pattern, expected",
        [
            ("foo", []),
            ("foo.foo", ["foo.foo"]),
            ("bar", []),
            ("bar.bar", ["bar.bar"]),
        ],
    )
    def test_search_file_strict_case(self, mock_db: Database, pattern, expected):
        """Verifies `search_file` method."""
        # Add various files
        for file_name in ["foo.bar", "bar.foo", "foo.foo", "bar.bar"]:
            self._helper_add_file(mock_db, file_name)

        # Search for string name pattern "foo"
        result = mock_db.search_file(self._dummy_user_id, pattern, strict_beg=True, strict_end=True)

        assert self._helper_compare_list_to_dict(expected, result, "file_name")

    def _helper_add_user(self, db: Database):
        """Add user helper."""
        query = "INSERT INTO users (user_name, password) VALUES(?, ?)"
        db._cursor.execute(query, [self._dummy_username, self._dummy_password])

    def _helper_add_file(self, db: Database, file_name: str = ""):
        """Add file helper."""
        query = "INSERT INTO files (file_name, file_type, file_size, user_id, created_at) VALUES (?, ?, ?, ?, ?)"
        created_at = datetime.datetime.now(datetime.UTC)
        file_name = self._dummy_file_name if not file_name else file_name
        db._cursor.execute(
            query,
            [file_name, self._dummy_file_type, self._dummy_file_size, self._dummy_user_id, created_at],
        )

    def _helper_delete_file(self, db: Database):
        """Delete file helper."""
        query = "DELETE FROM files WHERE user_id = ? AND file_name = ?"
        db._cursor.execute(query, [self._dummy_user_id, self._dummy_file_name])

    def _helper_check_file_exists(self, db: Database):
        """Check file exists helper."""
        return db._cursor.execute("SELECT * FROM files WHERE file_name = ?", [self._dummy_file_name]).fetchall()

    def _helper_compare_list_to_dict(self, a: List[str], b: List[dict[str, Any]], key: str) -> bool:
        """Compare list to dict helper."""
        match = True

        if len(a) != len(b):
            match = False

        if match:
            for i in range(len(a)):
                # check if key exists in the dict
                if key not in b[i]:
                    match = False

                # check if values at index matches
                elif a[i] != b[i][key]:
                    match = False

                else:
                    pass

                if match == False:
                    break

        return match


class DummyPasswordHashManager:
    """Implements (Dummy) password hash manager strategy class."""

    def generate_hash(self, password: str) -> str:
        """Generate (dummy) password hash."""
        return password

    def check_password(self, hash: str, password: str) -> bool:
        """Check (dummy) hash matches the password."""
        return hash == password
