"""Conftest."""

import os
import shutil
import sqlite3

import pytest
from werkzeug.datastructures import FileStorage

from cloud_storage.storage import Database, FileHandler

PATH_DEFINITIONS = {
    "db": "tests/db",
    "db_file": "test_db.sqlite",
    "storage": "tests/storage",
}


@pytest.fixture(scope="session", name="paths")
def get_paths():
    """Get configured paths."""
    return PATH_DEFINITIONS


#
# Setup and teardown paths
#


@pytest.fixture(scope="session", name="mock_db_dir_path")
def setup_and_teardown_db_dir():
    """Create (mock) database directory."""
    path = PATH_DEFINITIONS["db"]
    if not os.path.exists(path):
        os.mkdir(path)

    yield path

    os.rmdir(path)


@pytest.fixture(scope="session", name="storage_path")
def setup_and_teardown_storage_dir():
    """Create (mock) storage directory."""
    path = PATH_DEFINITIONS["storage"]
    if not os.path.exists(path):
        os.mkdir(path)

    yield path

    # shutil will remove non-empty path
    shutil.rmtree(path)


@pytest.fixture(scope="session", name="mock_db_path")
def setup_and_teardown_db_file(mock_db_dir_path):
    """Create (mock) sqlite database."""
    path = mock_db_dir_path + "/" + PATH_DEFINITIONS["db_file"]

    if not os.path.exists(path):
        open(path, "x")

    yield path

    os.remove(path)


#
# Initialization utils
#


@pytest.fixture(scope="session", name="sql_script")
def sqlite_schema_script() -> str:
    """Return sqlite schema script."""
    with open("cloud_storage/schema.sql", "r") as sql_file:
        sql_script = sql_file.read()

    return sql_script


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_mock_database(mock_db_path, sql_script):
    """Setup and teardown mock database"""
    db = sqlite3.connect(mock_db_path)
    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()

    yield


#
# Object factories
#


@pytest.fixture(scope="session", name="mock_db")
def fixture_database(mock_db_path):
    """Create instance of (mock) database."""
    return Database(mock_db_path)


@pytest.fixture(scope="session", name="mock_fm")
def fixture_file_handler(storage_path):
    """Create instance of (mock) file_handler."""
    return FileHandler(storage_path)


@pytest.fixture(scope="function", name="file")
def fixture_dummy_file():
    """Create (dummy) FileStorage type file."""
    name = "foo.txt"
    path = "tests/"
    file = open(path + name, "a+")

    yield FileStorage(file, name=name)

    os.remove(path + name)
