from flask import Flask

from flask_session import Session
from helpers import apology, login_required

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
