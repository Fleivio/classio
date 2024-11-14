from flask import *
from .index import has_active_token
from app.models import Lesson, Class, db, Token
from app.config import Config

class_ = Blueprint('class_', __name__)

@class_.post('/create_class')
def create_class():
    if has_active_token():
        
        class_name = request.form.get('class_name')
        class_description = request.form.get('class_description')

        cookie_token = request.cookies.get(Config.TOKEN_NAME)
        token = Token.query.filter_by(token=cookie_token).first()
        professor = token.user_id

        if not class_name or not class_description:
            return 'Missing class name or class description', 400

        lesson = Class(class_name=class_name, class_description=class_description, professor_id=professor)
        db.session.add(lesson)
        db.session.commit()

        return 'class created', 201
    else:
        return 'user not logged in', 401