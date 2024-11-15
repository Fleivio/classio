from app.models import Class, Lesson, db
from flask import *
from .index import get_active_token

lesson = Blueprint('lesson', __name__)

# GET 

@lesson.get('')
def lesson_get():
    lesson_id = request.args.get("lesson_id")
    lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()

    if not lesson:
        return 'sem lesson'

    class_ = Class.query.filter_by(class_id=lesson.class_id).first()

    if not class_:
        return 'sem class'
    
    print(class_.class_id)
    
    if not Class.usr_has_access_student(class_.class_id, get_active_token()):
        return 'sem acesso'

    return render_template("lesson/lesson.jinja", lesson_data=lesson.to_dict())

@lesson.get("/create")
def lesson_get_create():
    class_id = request.args.get("class_id")

    if not Class.usr_has_access_professor(class_id, get_active_token()):
        return redirect('/')

    class_ = Class.query.filter_by(class_id=class_id).first()

    if not class_:
        return redirect('/')

    return render_template("lesson/lesson_create.jinja", class_data=class_.to_dict())

@lesson.get('/edit')
def lesson_professor_get():
    lesson_id = request.args.get("lesson_id")
    lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()

    if not lesson:
        return redirect('/')

    class_ = Class.query.filter_by(class_id=lesson.class_id).first()

    if not class_:
        return redirect('/')
    
    print(class_.class_id)
    
    if not Class.usr_has_access_professor(class_.class_id, get_active_token()):
        return redirect('/')

    return render_template("lesson/lesson.jinja", lesson_data=lesson.to_dict())

# POST

@lesson.post("/create")
def lesson_post_create():
    class_id = request.args.get("class_id")

    if not Class.usr_has_access_professor(class_id, get_active_token()):
        return redirect('/')

    title = request.form.get("title")
    desc = request.form.get("lesson_description")

    lesson = Lesson(class_id=class_id, title=title, description=desc)
    db.session.add(lesson)
    db.session.commit()

    return redirect(f"/class?class_id={class_id}")
