from app.models import Class, db, Enrollment, Thread, Thread_Response, StatQuestion, StAnswer, Lesson
from flask import *
from .index import get_active_token
from datetime import datetime, timedelta, timezone

class_ = Blueprint('class_', __name__)

# GET

@class_.get('')
def class_get_class():
    class_id = request.args.get('class_id')

    class_ = Class.query.filter_by(class_id=class_id).first()

    if Class.usr_has_access_student(class_id, get_active_token()):
        return render_template("class/class_student.html", class_data=class_.to_dict(), class_=class_)

    if Class.usr_has_access_professor(class_id, get_active_token()):
        return render_template("class/class_professor.html", class_data=class_.to_dict(), class_=class_)

    return redirect('/')

@class_.get('/create')
def class_get_create():
    token = get_active_token()
    if not token:
        return redirect('/')

    return render_template("class/class_create.html")

@class_.get('/join')
def class_get_join():
    token = get_active_token()
    if not token:
        return redirect('/')
    return render_template("class/class_join.html")

@class_.get('/enrollments')
def class_get_enrollments():
    class_id = request.args.get('class_id')
    token = get_active_token()
    if not Class.usr_has_access_professor(class_id, token):
        return redirect('/')
    
    enrollments = Enrollment.query.filter_by(class_id=class_id).all()
    class_ = Class.query.filter_by(class_id=class_id).first()

    return render_template("class/class_enrollments.html", class_data=class_, enrollments=enrollments)

# POST

@class_.post('/create')
def class_post_create():
    token = get_active_token()
    
    if not get_active_token():
        return redirect('/')

    class_name = request.form.get('class_name')
    class_description = request.form.get('class_description')

    if not class_name or not class_description:
        return render_template("class/class_create.html")

    class_ = Class(class_name=class_name, class_description=class_description, professor_id=token.user_id)
    db.session.add(class_)
    db.session.commit()

    return redirect('/class?class_id=' + str(class_.class_id))

@class_.post('/delete')
def class_post_delete():
    token = get_active_token()
    class_id = request.args.get('class_id')
    
    if not Class.usr_has_access_professor(request.form.get('class_id'), token):
        return redirect('/')

    class_ = Class.query.filter_by(class_id=class_id).first()
    if not class_:
        return "Class not found or permission denied", 404

    db.session.delete(class_)
    db.session.commit()

    return redirect('/')

@class_.post('/edit')
def class_post_edit():
    token = get_active_token()
    class_id = request.args.get('class_id')
    
    if not Class.usr_has_access_professor(class_id, token):
        return redirect('/')
    
    class_ = Class.query.filter_by(class_id=class_id).first()
    if not class_:
        return "Class not found or permission denied", 404

    new_name = request.form.get('class_name')
    if new_name:
        class_.class_name = new_name

    new_description = request.form.get('class_description')
    if new_description:
        class_.class_description = new_description

    db.session.commit()

@class_.post('/join')
def class_post_join():
    token = get_active_token()
    if not token:
        return redirect('/')
    
    id = request.form.get('class_code')
    cl = Class.query.filter_by(class_id=id).first()
    if not id or not cl:
        flash('Invalid class code', 'error')
        return redirect('/class/join')

    cl = Class.query.filter_by(class_id=id).first()
    if not cl:
        flash('Class not found', 'error')
        return redirect('/class/join')
    
    if Class.usr_has_access_professor(id, get_active_token()):
        flash('You are the professor of this class', 'error')
        return redirect('/class/join')
    
    if Class.usr_has_access_student(id, get_active_token()):
        flash('You are already enrolled in this class', 'error')
        return redirect('/class/join')
    
    enrollment = Enrollment(user_id=token.user_id, class_id=id)
    db.session.add(enrollment)
    db.session.commit()

    return redirect('/class?class_id=' + str(id))

@class_.post("/kickout")
def class_post_kickout():
    class_id = request.args.get('class_id')
    user_id = request.args.get('user_id')

    token = get_active_token()
    if not (Class.usr_has_access_professor(class_id, token) or token.user_id == user_id):
        return "Unauthorized", 401

    enrollment = Enrollment.query.filter_by(class_id=class_id, user_id=user_id).first()
    if not enrollment:
        return redirect('/')
    
    db.session.delete(enrollment)
    db.session.commit()

    return redirect('/class/enrollments?class_id=' + class_id)

# ST Questions

@class_.post("st/create")
def class_post_create_st():
    class_id = request.args.get('class_id')
    token = get_active_token()

    if not Class.usr_has_access_professor(class_id, token):
        return ('no acc')
    
    title = request.form.get('st_title')
    if not title:
        return ('no tit')

    st = StatQuestion(class_id=class_id, title=title)
    db.session.add(st)
    db.session.commit()

    return redirect('/class?class_id=' + class_id)


@class_.post("/st/response")
def class_post_response_st():
    lesson_id = request.args.get('lesson_id')
    lesson = Lesson.query.filter_by(lesson_id = lesson_id).first()

    class_id = lesson.class_id

    token = get_active_token()
    uid = token.user_id

    if not Class.usr_has_access_student(class_id, token):
        return "no acc"
    

    resps = request.form.to_dict()

    for answ in resps:
        question_id = answ[3:]
        print(question_id)

        prevAns = StAnswer.query.filter_by(user_id=uid, question_id=question_id, lesson_id=lesson_id).first()

        if prevAns:
            prevAns.answer = resps[answ]
        else:
            answerObj = StAnswer(answer = resps[answ],
                            user_id=uid,
                            question_id=question_id,
                            lesson_id=lesson_id )
            db.session.add(answerObj)
            
    db.session.commit()
    
    return redirect('/lesson?lesson_id=' + lesson_id)
    


# THREADS

@class_.get('/thread/create')
def class_get_thread_create():
    class_id = request.args.get('class_id')
    token = get_active_token()
    if not Class.usr_has_access_student(class_id, token) and not Class.usr_has_access_professor(class_id, token):
        return redirect('/')
    
    class_ = Class.query.filter_by(class_id=class_id).first()

    return render_template("class/class_thread_create.html", class_=class_)

@class_.get('/thread')
def class_get_thread():
    thread_id = request.args.get('thread_id')
    token = get_active_token()
    thread = Thread.query.filter_by(thread_id=thread_id).first()
    class_ = Class.query.filter_by(class_id=thread.class_id).first()

    if Class.usr_has_access_student(class_.class_id, token):
        return render_template("class/class_thread_view.html", thread=thread, class_=class_)
    if Class.usr_has_access_professor(class_.class_id, token):
        return render_template("class/class_thread_view_professor.html", thread=thread, class_=class_)
        
    return redirect('/')

@class_.post('/thread/create')
def class_post_thread_create():
    class_id = request.args.get('class_id')
    token = get_active_token()

    if not Class.usr_has_access_student(class_id, token) and not Class.usr_has_access_professor(class_id, token):
        return 'no acess'
    
    thread_title = request.form.get('thread_title')
    thread_description = request.form.get('thread_desc')
    date_created = datetime.now(timezone(timedelta(hours=-3)))
    user_id = token.user_id

    thread = Thread(class_id=class_id
                    , title=thread_title
                    , description=thread_description
                    , date_created=date_created
                    , user_id=user_id)

    print(thread)

    db.session.add(thread)
    db.session.commit()


    return redirect('/class?class_id=' + class_id)

@class_.post('/thread/response')
def class_post_response():
    class_id = request.args.get('class_id')
    token = get_active_token()
    thread_id = request.args.get('thread_id')
    print("tid" + thread_id)

    if not Class.usr_has_access_student(class_id, token) and not Class.usr_has_access_professor(class_id, token):
        return redirect('/')
    
    response = request.form.get('response')
    date_now = datetime.now(timezone(timedelta(hours=-3)))
    uid = token.user_id


    response = Thread_Response(thread_id=thread_id
                    , response=response
                    , date_created=date_now
                    , user_id=uid)

    db.session.add(response)
    db.session.commit()
    return redirect('/class/thread?thread_id=' + thread_id)

@class_.post('/thread/delete')
def class_post_thread_delete():
    token = get_active_token()
    thread_id = request.args.get('thread_id')
    thread = Thread.query.filter_by(thread_id=thread_id).first()

    if not (Class.usr_has_access_professor(thread.class_id, token) or thread.user_id == token.user_id):
        return redirect('/')
    
    db.session.delete(thread)
    db.session.commit()
    return redirect('/')

@class_.post('/thread/edit')
def class_post_thread_edit():
    token = get_active_token()
    thread_id = request.args.get('thread_id')
   
    thread = Thread.query.filter_by(thread_id=thread_id, user_id=token.user_id).first()
    if not thread:
        return "Thread not found or permission denied", 404

    new_title = request.form.get('thread_title')
    if new_title:
        thread.title = new_title

    new_description = request.form.get('thread_description')
    if new_description:
        thread.description = new_description

    db.session.commit()
    return redirect('/')

@class_.post('/thread/response/edit')
def class_post_response_edit():
    token = get_active_token()
    response_id = request.args.get('response_id')
    response = Thread_Response.query.filter_by(response_id=response_id).first()

    if not (response.user_id == token.user_id):
        return redirect('/')
    
    new_response = request.form.get('response')
    response.response = new_response
    db.session.commit()
    return redirect('/')

@class_.post('/thread/response/delete')
def class_post_response_delete():
    token = get_active_token()
    response_id = request.args.get('response_id')
    response = Thread_Response.query.filter_by(response_id=response_id).first()

    if not (Class.usr_has_access_professor(response.thread.class_id, token) or response.user_id == token.user_id):
        return redirect('/')
    
    db.session.delete(response)
    db.session.commit()
    return redirect('/')
