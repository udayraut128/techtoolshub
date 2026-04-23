from flask import Blueprint, request, jsonify, render_template, send_file, current_app
import os
from app.services.file_service import handle_file_upload

file_share = Blueprint('file_share', __name__)


# Share page
@file_share.route("/share")
def share():
    return render_template("share.html")


# Upload
@file_share.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    files = request.files.getlist("file")

    if not files or files[0].filename == "":
        return jsonify({"error": "No files selected"})

    short_id, short_url, qr_filename = handle_file_upload(
        files,
        current_app.config['UPLOAD_FOLDER'],
        current_app.config['STATIC_FOLDER'],
        request.host_url
    )

    return jsonify({
        "url": short_url,
        "qr": f"/static/{qr_filename}"
    })


# Show download page
@file_share.route("/file/<short_id>")
def file_page(short_id):
    return render_template("download.html", file_id=short_id)


# Actual download (FIXED)
@file_share.route("/download/<short_id>")
def download_file(short_id):

    file_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        f"{short_id}.zip"
    )

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)

    return "File not found", 404