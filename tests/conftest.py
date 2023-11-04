"""Conftest."""

import os
import sqlite3

import pytest

from cloud_storage.storage import Database


@pytest.fixture(scope="session", name="mock_db_dir_path")
def fixture_mock_db_dir_path():
    path = "tests/db/"
    if not os.path.exists(path):
        os.mkdir(path)

    yield path

    os.rmdir(path)


@pytest.fixture(scope="session", name="mock_db_path")
def fixture_mock_db_path(mock_db_dir_path):
    path = mock_db_dir_path + "test_db.sqlite"

    if not os.path.exists(path):
        open(path, "x")

    yield path

    os.remove(path)

@pytest.fixture(scope="session", name="sql_script")
def sqlite_schema() -> str:
    with open("cloud_storage/schema.sql", "r") as sql_file:
        sql_script = sql_file.read()

    return sql_script 

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_dummy_database(mock_db_path, sql_script):
    """"""
    db = sqlite3.connect(mock_db_path)
    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()

    yield


@pytest.fixture(scope="session", name="mock_db")
def fixture_database(mock_db_path):
    """Create instance of (mock) database."""
    return Database(mock_db_path)
