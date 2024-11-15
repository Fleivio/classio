from app.models import Class
from flask import Blueprint, render_template

lesson = Blueprint('lesson', __name__)

@lesson.get("/<class_id>/create")
def lesson_get_create(class_id):
    class_name = Class.query.filter_by(class_id=class_id).first().class_name
    return render_template("lesson_create.jinja", class_name=class_name)
