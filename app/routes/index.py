from flask import * 
from app.config import Config
from app.models import Token, Class, Enrollment

index = Blueprint('index', __name__)

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
        return render_template("index.jinja")
    
@index.get("/login")
def login_get():
    if get_active_token():
        return redirect("/")
    return render_template("login.jinja")

@index.get("/signup")
def signup_get():
    if get_active_token():
        return redirect("/")
    return render_template("sign_up.jinja")

@index.get("/home")
def user_home():
    token = get_active_token()

    if not token:
        return redirect("/")
    
    uid = token.user_id

    student_enrollments = Enrollment.query.filter_by(student_id=uid).all()

    user_classes_student = map(lambda elem: elem.class_, student_enrollments)
    user_classes_professor = Class.query.filter_by(professor_id=uid).all()

    def class_to_dict(elem):
        return {
            'class_name': elem.class_name,
            'class_description': elem.class_description,
            'class_id': str(elem.class_id)
        }

    user_data = {
        'classes_student': 
            list(map(class_to_dict, user_classes_student)),
        'classes_professor': 
            list(map(class_to_dict, user_classes_professor))
    }

    print(user_data)

    return render_template("index_logged.jinja",user_data=user_data)
