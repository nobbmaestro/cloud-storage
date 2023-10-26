"""Implements Application."""

from flask import Flask

from cloud_storage.common import Database
from flask_session import Session


# Configure application
def create_app() -> Flask:
    """Create and configure the application."""
    app = Flask(__name__)

    # Initialize the database isntance
    app.config["DATABASE"] = Database("cloud.db")

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    return app


# Create application object
app = create_app()


@app.after_request
def after_request(response):
    """Ensure response are not cached."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# This is awkward, but this is according to Flash docs
#   source: https://flask.palletsprojects.com/en/3.0.x/patterns/packages/
import cloud_storage.views
import cloud_storage.auth
