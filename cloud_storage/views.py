"""Views."""

from cloud_storage import app
from cloud_storage.common import apology, login_required


@app.route("/")
@login_required
def index():
    """Show homepage."""
    return apology("TODO")
