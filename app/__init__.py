from flask import Flask
import os
from .routes.views import main
from .routes.user import user

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    app.register_blueprint(main)
    app.register_blueprint(user)

    return app