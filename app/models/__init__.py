from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .model_user import User
from .model_token import Token
from .model_class import Class
from .model_enrollment import Enrollment
from .model_lesson import Lesson