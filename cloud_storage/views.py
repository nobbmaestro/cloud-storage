"""Views."""

from flask import (flash, redirect, render_template, request, send_file,
                   session, url_for)
from werkzeug.utils import secure_filename

from cloud_storage import app, storage_handler
from cloud_storage.common import apology, login_required


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show homepage."""

    if request.method == "POST":
        return apology("TODO")

    else:
        storage = storage_handler._db.get_list_of_files(session["user_id"])
        return render_template("index.html", storage=storage)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """Upload file to the cloud storage."""
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file:
            file_name = secure_filename(file.filename)
            success = storage_handler.upload_file(session["user_id"], file)
            if success:
                flash("'%s' uploaded" % file_name)
            else:
                return apology("Something went wrong")

            return redirect(url_for("upload", name=file_name))

    else:
        return render_template("upload_file.html")


@app.route("/download", methods=["GET"])
@login_required
def download():
    """Download file to the cloud storage."""
    file_name = request.args.get("file_name")
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
    file_name = request.args.get("file_name")
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
