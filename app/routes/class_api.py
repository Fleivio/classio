from app.models import Class, db
from flask import Blueprint, request, render_template

from app.models.model_lesson import Lesson

from .index import get_active_token

class_ = Blueprint('class_', __name__)

@class_.get('')
def class_get_class():
    class_id = request.args.get('class_id')
    class_ = Class.query.filter_by(class_id=class_id).first()
    lessons = Lesson.query.filter_by(class_id=class_id).all() 

    data = {
        "class_": class_,
        "lessons": lessons
    }

    return render_template("class_professor.jinja", data=data)

@class_.get('/lesson')
def class_get_lesson():
    return "doaijsdoi"

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
