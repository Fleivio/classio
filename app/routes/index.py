from app.config import Config
from app.models import Class, Enrollment, Token, User
from flask import Blueprint, redirect, render_template, request

index = Blueprint("index", __name__)


def get_active_token():
    cookie_token = request.cookies.get(Config.TOKEN_NAME)
    token = Token.query.filter_by(token=cookie_token).first()

    if token and not token.expired():
        return token
    return None


@index.route("/")
def index_screen():
    if get_active_token():
        return redirect("/home")
    else:
        return render_template("home/index.html")


@index.get("/login")
def login_get():
    if get_active_token():
        return redirect("/")
    return render_template("home/login.html")


@index.get("/signup")
def signup_get():
    if get_active_token():
        return redirect("/")
    return render_template("home/sign_up.html")


@index.get("/home")
def user_home():
    token = get_active_token()

    if not token:
        return redirect("/")

    uid = token.user_id

    student_enrollments = Enrollment.query.filter_by(user_id=uid).all()

    user_classes_student = map(lambda elem: elem.class_, student_enrollments)
    user_classes_professor = Class.query.filter_by(professor_id=uid).all()

    def class_to_dict(elem):
        return {
            "class_name": elem.class_name,
            "class_description": elem.class_description,
            "class_id": str(elem.class_id),
        }

    user = User.query.filter_by(user_id=uid).first()

    user_data = {
        "classes_student": list(map(class_to_dict, user_classes_student)),
        "classes_professor": list(map(class_to_dict, user_classes_professor)),
        "username": user.username,
    }

    return render_template("home/index_logged.html", user_data=user_data)
