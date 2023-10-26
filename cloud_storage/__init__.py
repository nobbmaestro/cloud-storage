"""Implements Application."""

from flask import Flask

from flask_session import Session

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure databse
# TODO


@app.after_request
def after_request(response):
    """Ensure response are not cached."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# This is awkward, but this is according to Flash docs: https://flask.palletsprojects.com/en/3.0.x/patterns/packages/
import cloud_storage.views
