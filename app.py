from flask import Flask, render_template, request
import qrcode
import random
import string

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# QR Code Generator
@app.route("/qr", methods=["GET", "POST"])
def qr():
    qr_image = None
    if request.method == "POST":
        url = request.form["url"]
        img = qrcode.make(url)
        path = "static/qr.png"
        img.save(path)
        qr_image = path

    return render_template("qr.html", qr_image=qr_image)


if __name__ == "__main__":
    app.run(debug=True)