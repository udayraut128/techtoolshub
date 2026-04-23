from flask import Blueprint, send_from_directory, render_template

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")


@main.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")


@main.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml")