"""Authentication."""

from flask import redirect, render_template, request, session

from cloud_storage import app, storage_handler
from cloud_storage.common import apology, validate_password

# Obtain the database object
db = app.config["DATABASE"]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Signup user."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure that password matches confirmation
        elif password != confirmation:
            return apology("password must match", 400)

        # Validate password complexity
        elif not validate_password(password):
            return apology("not sufficient password", 400)

        # Create user storage area
        if not storage_handler.add_user(username, password):
            return apology("username already exists")

        # Redirect iser to home page
        return redirect("/")

    else:
        return render_template("signup.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Verify user credentials
        if not storage_handler._db.check_user_credentials(username, password):
            return apology("invalid username anr/or password", 403)

        # Remember which user has logged in
        session["user_id"] = storage_handler._db.get_user_id(username)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
