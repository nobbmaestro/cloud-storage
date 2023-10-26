"""Authentication."""

from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from cloud_storage import app
from cloud_storage.common import apology, validate_password

# Obtain the database object
db = app.config["DATABASE"]


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

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

        # Check whether username already exists, insert to database if no matches exists
        result = db.execute_query("SELECT username FROM users WHERE username=?", [username])
        if result:
            return apology("username already exists", 400)

        else:
            # Create password hash
            hash = generate_password_hash(password)

            # Insert user into the database
            values = (username, hash)
            db.execute_query("INSERT INTO users (username, hash) VALUES(?, ?)", values)
            db.commit()

        # Redirect iser to home page
        return redirect("/")

    else:
        return render_template("register.html")


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
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute_query("SELECT * FROM users WHERE username = ?", [request.form.get("username")])

        print(rows[0]["hash"])
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
