"""Utilities."""

from flask import flash, redirect, request, send_file, session

from cloud_storage import app, storage_handler
from cloud_storage.common import login_required, purge_list


@app.route("/download", methods=["GET"])
@login_required
def download():
    """Download file to the cloud storage."""
    file_name = request.args.get("query", "")
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


@app.route("/delete", methods=["GET"])
@login_required
def delete():
    """Delete file(s) from the cloud storage."""
    file_names = request.args.get("query", "").split(",")

    # Sanitize the list of names
    file_names = purge_list(file_names)

    # Ensure file_name is specified in the URL
    if not file_names:
        flash("No file selected")

    else:
        try:
            if storage_handler.delete_file(session["user_id"], file_names):
                flash("Deleted")
            else:
                flash("Something went wrong", category="error")

        except FileNotFoundError as error:
            flash(str(error))

    return redirect("/")
