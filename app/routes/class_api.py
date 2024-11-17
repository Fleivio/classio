from app.models import Class, db, Enrollment
from flask import *
from .index import get_active_token

class_ = Blueprint('class_', __name__)

# GET

@class_.get('')
def class_get_class():
    class_id = request.args.get('class_id')

    if not Class.usr_has_access_student(class_id, get_active_token()):
        return redirect('/')

    class_ = Class.query.filter_by(class_id=class_id).first()

    return render_template("class/class_student.html", class_data=class_.to_dict())

@class_.get('/edit')
def class_get_edit():
    class_id = request.args.get('class_id')

    if not Class.usr_has_access_professor(class_id, get_active_token()):
        return redirect('/')

    class_ = Class.query.filter_by(class_id=class_id).first()

    return render_template("class/class_professor.html", class_data=class_.to_dict())

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

    return redirect('/class/edit?class_id=' + str(class_.class_id))

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

    if not Class.usr_has_access_professor(class_id, get_active_token()):
        return "Unauthorized", 401

    enrollment = Enrollment.query.filter_by(class_id=class_id, user_id=user_id).first()
    if not enrollment:
        return redirect('/')
    
    db.session.delete(enrollment)
    db.session.commit()

    return redirect('/class/enrollments?class_id=' + class_id)

@class_.post('/edit_params')
def edit_class_name():
    print('aaaaa')

    if not Class.usr_has_access_professor(request.args.get('class_id'), get_active_token()):
        return redirect('/')

    data = request.get_json()
    class_id = data.get('class_id')
    new_name = data.get('class_name')
    new_desc = data.get('class_desc')

    print(class_id, new_name)

    class_instance = Class.query.get(class_id)
    if class_instance:
        class_instance.class_name = new_name
        class_instance.class_description = new_desc
        db.session.commit()
        return jsonify({"message": "Class name updated successfully"}), 200
    else:
        return jsonify({"error": "Class not found"}), 404