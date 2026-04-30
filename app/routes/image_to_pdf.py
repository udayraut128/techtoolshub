from flask import Blueprint, render_template, request, send_file
from PIL import Image
import os
import uuid

image_to_pdf = Blueprint("image_to_pdf", __name__)

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
PDF_FOLDER = os.path.join(BASE_DIR, "converted")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)


@image_to_pdf.route("/image-to-pdf", methods=["GET", "POST"])
def home():

    pdf_file = None

    if request.method == "POST":

        files = request.files.getlist("images")

        image_list = []

        unique_name = str(uuid.uuid4())
        pdf_filename = unique_name + ".pdf"

        pdf_path = os.path.join(PDF_FOLDER, pdf_filename)

        for file in files:

            if file.filename == "":
                continue

            image_path = os.path.join(
                UPLOAD_FOLDER,
                file.filename
            )

            file.save(image_path)

            image = Image.open(image_path).convert("RGB")

            image_list.append(image)

        if image_list:

            first_image = image_list[0]

            remaining_images = image_list[1:]

            first_image.save(
                pdf_path,
                save_all=True,
                append_images=remaining_images
            )

            pdf_file = pdf_filename

    return render_template(
        "image_to_pdf.html",
        pdf_file=pdf_file
    )


@image_to_pdf.route("/download-pdf/<file>")
def download_pdf(file):

    path = os.path.join(PDF_FOLDER, file)

    return send_file(
        path,
        as_attachment=True
    )