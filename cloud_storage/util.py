"""Utilities."""

from flask import flash, redirect, request, send_file, session

from cloud_storage import app, storage_handler
from cloud_storage.common import login_required


@app.route("/download", methods=["GET"])
@login_required
def download():
    """Download file to the cloud storage."""
    file_name = request.args.get("file_name", "")
    path = storage_handler.get_file_path(session["user_id"], file_name)

    # Ensure file_name is specified in the URL
    if not file_name:
        flash("File name not given")

    # Ensure file_name exists
    elif not path:
        flash("File not found")

    else:
        try:
            return send_file(path, as_attachment=True)

        except:
            flash("Something went wrong", category="error")

    return redirect("/")

@app.route("/remove", methods=["GET"])
@login_required
def remove():
    """Remove file from the cloud storage."""
    file_name = request.args.get("file_name", "")
    path = storage_handler.get_file_path(session["user_id"], file_name)

    # Ensure file_name is specified in the URL
    if not file_name:
        flash("File name not given")

    # Ensure file_name exists
    elif not path:
        flash("File not found")

    else:
        if storage_handler.remove_file(session["user_id"], file_name):
            flash("File '%s' removed" % file_name)
        else:
            flash("Something went wrong", category="error")

    return redirect("/")
