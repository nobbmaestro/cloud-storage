"""Implements helpers function"""

import logging
import re
from functools import wraps

from flask import redirect, render_template, session

logger = logging.getLogger(__name__)


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

    return render_template("misc/apology.html", top=code, bottom=escape(message)), code


def validate_password(password):
    """Validate user password."""
    special_chars = ("$", "#", "@", "!", "*")

    # Check password length
    if len(password) < 10:
        valid = False
        logger.info("Password validation: length not sufficient")

    # Check weather password contains digits
    elif re.search("[0-9]", password) is None:
        valid = False
        logger.info("Password validation: no digits")

    # Check weather password contains uppercase characters
    elif re.search("[A-Z]", password) is None:
        valid = False
        logger.info("Password validation: no uppercase")

    # Check weather password contains special characters
    elif not any(c in special_chars for c in password):
        valid = False
        logger.info("Password validation: no special chars")

    # Above fulfilled, password is valid
    else:
        valid = True

    return valid
