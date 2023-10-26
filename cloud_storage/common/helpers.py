"""Implements helpers function"""

import re
from functools import wraps

from flask import redirect, render_template, session


def login_required(func):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return func(*args, **kwargs)

    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def validate_password(password):
    """Validate user password."""
    special_chars = ("$", "#", "@", "!", "*")

    # Check password length
    if len(password) < 10:
        print("Password validation: length not sufficient")
        valid = False

    # Check weather password contains digits
    elif re.search("[0-9]", password) is None:
        print("Password validation: no digits")
        valid = False

    # Check weather password contains uppercase characters
    elif re.search("[A-Z]", password) is None:
        print("Password validation: no uppercase")
        valid = False

    # Check weather password contains special characters
    elif not any(c in special_chars for c in password):
        print("Password validation: no special chars")
        valid = False

    # Above fulfilled, password is valid
    else:
        valid = True

    return valid
