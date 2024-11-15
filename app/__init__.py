import os

from flask import Flask
from flask_migrate import Migrate

from app.models import db
from app.routes.class_api import class_
from app.routes.index import index
from app.routes.user_api import user
from app.routes.lesson_api import lesson

from .config import Config


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(index)
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(class_, url_prefix='/class')
    app.register_blueprint(lesson, url_prefix='/lesson')

    return app
