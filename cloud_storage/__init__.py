"""Implements Application."""

from flask import Flask

from cloud_storage.common import (FileHandler, StorageHandler,
                                  pretty_file_size_format,
                                  pretty_relative_datetime_format)
from cloud_storage.database import Database
from flask_session import Session


# Configure application
def create_app() -> Flask:
    """Create and configure the application."""
    app = Flask(__name__)

    # Configure custom filters
    app.jinja_env.filters["file_size"] = pretty_file_size_format
    app.jinja_env.filters["rel_dtime"] = pretty_relative_datetime_format

    # Initialize the database isntance
    app.config["DATABASE"] = Database("db.sqlite")

    # Configure the file storage location
    app.config["UPLOAD_FOLDER"] = "/Users/norbertbatiuk/CloudStorage"

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    return app


# Create application object
app = create_app()
db = Database("db.sqlite")
fm = FileHandler(app, "/Users/norbertbatiuk/CloudStorage/")
storage_handler = StorageHandler(app, db, fm)


@app.after_request
def after_request(response):
    """Ensure response are not cached."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# This is awkward, but this is according to Flash docs
#   source: https://flask.palletsprojects.com/en/3.0.x/patterns/packages/
import cloud_storage.auth
import cloud_storage.util
import cloud_storage.views
