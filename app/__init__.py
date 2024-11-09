from flask import Flask
import os
from .routes.lesson import lesson
from .routes.user import user

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    app.register_blueprint(lesson)
    app.register_blueprint(user)

    return app