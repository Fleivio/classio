from flask import Flask
from flask_migrate import Migrate
import os

from config import Config

from app.routes.lesson import lesson
from app.routes.user import user
from app.routes.debug import debug

from app.models.models import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(lesson)
    app.register_blueprint(user)
    app.register_blueprint(debug)

    return app