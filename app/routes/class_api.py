from app.models import Class, db, Enrollment
from flask import *
from .index import get_active_token

class_ = Blueprint('class_', __name__)

@class_.get('')
def class_get_class():
    class_id = request.args.get('class_id')

    if not Class.usr_has_access_student(class_id, get_active_token()):
        return redirect('/')

    class_ = Class.query.filter_by(class_id=class_id).first()

    return render_template("class/class_student.jinja", class_data=class_.to_dict())

@class_.get('/edit')
def class_get_edit():
    class_id = request.args.get('class_id')

    if not Class.usr_has_access_professor(class_id, get_active_token()):
        return redirect('/')

    class_ = Class.query.filter_by(class_id=class_id).first()

    return render_template("class/class_professor.jinja", class_data=class_.to_dict())

# @class_.put('/edit')
# def class_put_edit():
#     class_id = request.args.get('class_id')

#     if not Class.usr_has_access_professor(class_id, get_active_token()):
#         return redirect('/')

#     class_name = request.form.get('class_name')
#     class_description = request.form.get('class_description')

#     if not class_name or not class_description:
#         return redirect('/class/edit?class_id=' + class_id)
    
#     class_ = Class.query.filter_by(class_id=class_id).first()
#     class_.class_name = class_name
#     class_.class_description = class_description
#     db.session.commit()

#     return redirect('/class/edit?class_id=' + class_id)

@class_.post('/create')
def class_post_create():
    token = get_active_token()
    
    if not get_active_token():
        return redirect('/')

    class_name = request.form.get('class_name')
    class_description = request.form.get('class_description')

    if not class_name or not class_description:
        return render_template("class/class_create.jinja")

    class_ = Class(class_name=class_name, class_description=class_description, professor_id=token.user_id)
    db.session.add(class_)
    db.session.commit()

    return redirect('/class/edit?class_id=' + str(class_.class_id))

@class_.get('/create')
def class_get_create():
    token = get_active_token()
    if not token:
        return redirect('/')

    return render_template("class/class_create.jinja")

@class_.get('/join')
def class_get_join():
    token = get_active_token()
    if not token:
        return redirect('/')
    return render_template("class/class_join.jinja")

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
    
    enrollment = Enrollment(student_id=token.user_id, class_id=id)
    db.session.add(enrollment)
    db.session.commit()

    return redirect('/class?class_id=' + str(id))
