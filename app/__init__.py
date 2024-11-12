from flask import Flask
from flask_migrate import Migrate
import os

from .config import Config
from mvc_flask import FlaskMVC

from app.models import db

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    FlaskMVC(app)

    return app