from app.models import Class, Lesson, db, Question, Answer
from flask import *
from .index import get_active_token
from datetime import datetime, timedelta, timezone

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

    questions = Question.query.filter_by(lesson_id=lesson_id).all()

    return render_template("lesson/lesson_student.html", lesson=lesson, questions=questions)

@lesson.get("/create")
def lesson_get_create():
    class_id = request.args.get("class_id")

    if not Class.usr_has_access_professor(class_id, get_active_token()):
        return redirect('/')

    class_ = Class.query.filter_by(class_id=class_id).first()

    if not class_:
        return redirect('/')

    return render_template("lesson/lesson_create.html", class_data=class_.to_dict())

@lesson.get('/edit')
def lesson_professor_get():
    lesson_id = request.args.get("lesson_id")
    lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()

    if not lesson:
        return redirect('/')

    class_ = Class.query.filter_by(class_id=lesson.class_id).first()

    if not class_:
        return redirect('/')
    
    if not Class.usr_has_access_professor(class_.class_id, get_active_token()):
        return redirect('/')

    questions = Question.query.filter_by(lesson_id=lesson_id).all()

    return render_template("lesson/lesson_edit.html", lesson=lesson, questions=questions)

@lesson.get("/answers")
def lesson_get_answers():
    return ""

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

    return redirect(f"/lesson/edit?lesson_id={lesson.lesson_id}")

@lesson.post("/edit")
def lesson_post_edit():
    lesson_id = request.args.get("lesson_id")
    return redirect(f"/lesson/edit?lesson_id={lesson_id}")

@lesson.post("/add_question")
def lesson_post_question():
    lesson_id = request.args.get("lesson_id")

    if not lesson_id:
        return redirect('/')
    
    lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()

    if not lesson:
        return redirect('/')
    
    class_ = lesson.class_id

    if not Class.usr_has_access_professor(class_, get_active_token()):
        return redirect('/')

    title = request.form.get("question_title")
    question = request.form.get("question_description")
    date_created = datetime.now(timezone.utc) 

    question = Question(lesson_id=lesson_id, title=title, description=question, date_created=date_created, is_multiple_choice=False)
    db.session.add(question)
    db.session.commit()

    return redirect(f"/lesson/edit?lesson_id={lesson_id}")

@lesson.post("/add_answers")
def lesson_post_add_answers():
    lesson_id = request.args.get("lesson_id")
    question_id = request.args.get("question_id")
    
    lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()

    if not lesson:
        return redirect('/')
    
    class_ = lesson.class_id

    if not Class.usr_has_access_student(class_, get_active_token()):
        return redirect('/')
    
    answer = request.form.get("answer")
    uid = get_active_token().user_id
    date_now = datetime.now(timezone.utc)
    answer = Answer(answer=answer, 
                    date_created=date_now,
                    user_id=uid,
                    question_id=question_id)
        
    db.session.add(answer)
    db.session.commit()

    return redirect(f"/lesson?lesson_id={lesson_id}")
