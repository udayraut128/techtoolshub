from flask import Flask, app, typing
import os

from app.routes import image_to_pdf, mp3_converter

def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, "uploads")
    app.config['STATIC_FOLDER'] = os.path.join(BASE_DIR, "app/static")

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register routes
    from .routes.main import main
    from .routes.qr import qr
    from .routes.group import group
    from .routes.file_share import file_share
    from .routes.clipboard import clipboard
    from .routes.date_converter import date_converter
    from .routes.typing import typing
    from .routes.mp3_converter import mp3_converter
    from .routes.image_to_pdf import image_to_pdf

    app.register_blueprint(main)
    app.register_blueprint(qr)
    app.register_blueprint(group)
    app.register_blueprint(file_share)
    app.register_blueprint(clipboard)
    app.register_blueprint(date_converter)
    app.register_blueprint(typing)
    app.register_blueprint(mp3_converter)
    app.register_blueprint(image_to_pdf)
    

    return app