from flask import Flask
from flask_migrate import Migrate
import os

from .config import Config

from app.models import db
from app.routes.debug import debug

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(debug, url_prefix='/debug')

    return app