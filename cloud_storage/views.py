"""Implements views."""

from cloud_storage import app
from cloud_storage.common import apology, login_required


@app.route("/")
@login_required
def index():
    """Show homepage."""
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    return apology("TODO")


@app.route("/logout")
def logout():
    """Log user out."""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    return apology("TODO")
