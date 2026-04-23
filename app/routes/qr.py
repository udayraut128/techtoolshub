from flask import Blueprint, render_template, request
import qrcode, os, random, string
from flask import current_app

qr = Blueprint('qr', __name__)

@qr.route("/qr", methods=["GET", "POST"])
def qr_page():
    qr_image = None

    if request.method == "POST":
        url = request.form["url"]

        img = qrcode.make(url)

        filename = ''.join(random.choices(string.ascii_letters, k=6)) + ".png"
        path = os.path.join(current_app.config['STATIC_FOLDER'], filename)
        img.save(path)

        qr_image = f"/static/{filename}"

    return render_template("qr.html", qr_image=qr_image)