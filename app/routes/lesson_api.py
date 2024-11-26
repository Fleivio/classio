from app.models import Class, Lesson, db, Question, Answer, StAnswer, StatQuestion
from flask import request, render_template, redirect, Blueprint
from .index import get_active_token
from datetime import datetime, timedelta, timezone

lesson = Blueprint("lesson", __name__)

# GET

@lesson.get("")
def lesson_get():
    lesson_id = request.args.get("lesson_id")
    lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()

    if not lesson:
        return "sem lesson"

    class_ = Class.query.filter_by(class_id=lesson.class_id).first()

    if not class_:
        return "sem class"

    questions = Question.query.filter_by(lesson_id=lesson_id).all()

    if Class.usr_has_access_student(class_.class_id, get_active_token()):
        uid = get_active_token().user_id
        answers = Answer.query.filter_by(user_id=uid).all()

        answers_dict = {}
        for answer in answers:
            answers_dict[answer.question_id] = answer.answer

        st_questions = class_.st_questions

        st_answers_dict = {}
        for st_question in st_questions:
            st_answer = StAnswer.query.filter_by(
                                                user_id = uid,
                                                question_id = st_question.st_question_id,
                                                lesson_id=lesson_id).first()
            rank = 3 if not st_answer else st_answer.answer
            st_answers_dict[st_question.st_question_id] = rank
        
        # print("a", st_answers_dict)

        return render_template(
            "lesson/lesson_student.html",
            lesson=lesson,
            questions=questions,
            answers=answers_dict,
            st_questions=class_.st_questions,
            st_answers=st_answers_dict
        )

    if Class.usr_has_access_professor(class_.class_id, get_active_token()):
        return render_template(
            "lesson/lesson_edit.html", lesson=lesson, questions=questions
        )

    return redirect("/")


@lesson.get("/create")
def lesson_get_create():
    class_id = request.args.get("class_id")

    if not Class.usr_has_access_professor(class_id, get_active_token()):
        return redirect("/")

    class_ = Class.query.filter_by(class_id=class_id).first()

    if not class_:
        return redirect("/")

    return render_template("lesson/lesson_create.html", class_data=class_.to_dict())


@lesson.get("/answers")
def lesson_get_answers():
    question_id = request.args.get("question_id")

    # :|
    question = Question.query.filter_by(question_id=question_id).first()
    lesson = Lesson.query.filter_by(lesson_id=question.lesson_id).first()
    class_ = Class.query.filter_by(class_id=lesson.class_id).first()
    answers = Answer.query.filter_by(question_id=question_id).all()

    return render_template(
        "lesson/lesson_answers.html",
        class_=class_,
        lesson=lesson,
        answers=answers,
        question=question,
    )


# POST


@lesson.post("/create")
def lesson_post_create():
    class_id = request.args.get("class_id")

    if not Class.usr_has_access_professor(class_id, get_active_token()):
        return redirect("/")

    title = request.form.get("title")
    desc = request.form.get("lesson_description")

    lesson = Lesson(class_id=class_id, title=title, description=desc)
    db.session.add(lesson)
    db.session.commit()

    return redirect(f"/lesson?lesson_id={lesson.lesson_id}")


@lesson.post("/edit")
def lesson_post_edit():
    lesson_id = request.args.get("lesson_id")
    return redirect(f"/lesson?lesson_id={lesson_id}")


@lesson.post("/add_question")
def lesson_post_question():
    lesson_id = request.args.get("lesson_id")

    if not lesson_id:
        return redirect("/")

    lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()

    if not lesson:
        return redirect("/")

    class_ = lesson.class_id

    if not Class.usr_has_access_professor(class_, get_active_token()):
        return redirect("/")

    title = request.form.get("question_title")
    question = request.form.get("question_description")
    date_created = datetime.now(timezone(timedelta(hours=-3)))

    question = Question(
        lesson_id=lesson_id,
        title=title,
        description=question,
        date_created=date_created,
        is_multiple_choice=False,
    )
    db.session.add(question)
    db.session.commit()

    return redirect(f"/lesson?lesson_id={lesson_id}")


@lesson.post("/add_answers")
def lesson_post_add_answers():
    lesson_id = request.args.get("lesson_id")
    question_id = request.args.get("question_id")

    lesson = Lesson.query.filter_by(lesson_id=lesson_id).first()

    if not lesson:
        return redirect("/")

    class_ = lesson.class_id

    if not Class.usr_has_access_student(class_, get_active_token()):
        return redirect("/")

    answer = request.form.get("answer")
    uid = get_active_token().user_id
    date_now = datetime.now(timezone(timedelta(hours=-3)))
    answer = Answer(
        answer=answer, date_created=date_now, user_id=uid, question_id=question_id
    )

    db.session.add(answer)
    db.session.commit()

    return redirect(f"/lesson?lesson_id={lesson_id}")
