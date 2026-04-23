from flask import Flask, app
import os

def create_app():
    app = Flask(__name__)

    # Config
    

    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, "uploads")
    app.config['STATIC_FOLDER'] = os.path.join(BASE_DIR, "app/static")
    app.config['STATIC_FOLDER'] = "app/static"

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register routes
    from .routes.main import main
    from .routes.qr import qr
    from .routes.group import group
    from .routes.file_share import file_share

    app.register_blueprint(main)
    app.register_blueprint(qr)
    app.register_blueprint(group)
    app.register_blueprint(file_share)

    return app