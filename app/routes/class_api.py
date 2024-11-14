from app.models import Class, db
from flask import Blueprint, request, render_template

from .index import get_active_token

class_ = Blueprint('class_', __name__)

@class_.post('/create')
def create():
    token = get_active_token()
    
    if not get_active_token():
        return 'user not logged in', 401

    class_name = request.form.get('class_name')
    class_description = request.form.get('class_description')

    professor = token.user_id

    if not class_name or not class_description:
        return 'Missing class name or class description', 400

    lesson = Class(class_name=class_name, class_description=class_description, professor_id=professor)
    db.session.add(lesson)
    db.session.commit()

    return 'class created', 201

@class_.get('/create')
def class_get_create():
    return render_template("class_create.jinja")

@class_.get('/join')
def class_get_join():
    return render_template("class_join.jinja")
