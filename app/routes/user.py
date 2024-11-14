from datetime import datetime, timezone
from flask import * 
from app.config import Config
from app.models import User, Token, Class, Enrollment, db

user = Blueprint('user', __name__)

@user.post("/login")
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return 'Missing email or password', 400
    
    u = User.query.filter_by(email=email).first()

    if not u:
        return 'User not found', 404
    
    if not u.check_password(password):
        return 'Invalid password', 401
    
    token = Token.generate_token(u)
    response = make_response(redirect("/"))
    response.set_cookie(Config.TOKEN_NAME, token.token)
    return response

@user.post("/signup")
def signup_post():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    user = User(username=username, email=email, hash_password=User.create_password_hash(password))
    db.session.add(user)
    db.session.commit()

    token = Token.generate_token(user)

    response = make_response(redirect("/"))
    response.set_cookie(Config.TOKEN_NAME, token.token)
    return response

@user.route('/logout')
def logout():
    cookie_token = request.cookies.get(Config.TOKEN_NAME)

    token = Token.query.filter_by(token=cookie_token).first()
    if token:
        db.session.delete(token)
        db.session.commit()

    response = make_response(redirect("/"))
    response.set_cookie(Config.TOKEN_NAME, '', expires=0)
    return response

@user.get("/home")
def user_home():
    tk = request.cookies.get(Config.TOKEN_NAME)
    token = Token.query.filter_by(token=tk).first()


    if not token or token.expired():
        return redirect("/")
    
    uid = token.user_id

    student_enrollments = Enrollment.query.filter_by(student_id=uid).all()

    user_classes_student = map(lambda elem: elem.class_, student_enrollments)
    user_classes_professor = Class.query.filter_by(professor_id=uid).all()

    return render_template("index_logged.jinja",user_data=[])
