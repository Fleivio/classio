from flask import * 
from app.config import Config
from app.models import User, Token, db

user = Blueprint('user', __name__)

def is_logged():
    token = request.cookies.get(Config.TOKEN_NAME)
    if token:
        # adicionar verificação da validade do token
        return True
    return False

@user.route("/")
def index_screen():
    if is_logged():
        user_data = {
            'name': 'PIMTO',
            'classes_professor': [
                { 'name': 'Turma de Teste 1', 'class_id' : 'CLASS_TEST_ID'},
                { 'name': 'Turma de Teste 2', 'class_id' : 'CLASS_TEST_ID'}
                ],
            'classes_student': [
                { 'name': 'Turma de Teste 3', 'class_id' : 'CLASS_TEST_ID'},
                { 'name': 'Turma de Teste 4', 'class_id' : 'CLASS_TEST_ID'}
                ]
            
        }

        return render_template("index_logged.jinja",user_data=user_data)
    else:
        return render_template("index.jinja")
    
@user.get("/login")
def login_get():
    if is_logged():
        return redirect("/")
    return render_template("login.jinja")

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

@user.get("/signup")
def signup_get():
    if is_logged():
        return redirect("/")
    return render_template("sign_up.jinja")

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
    response = make_response(redirect("/"))
    response.set_cookie(Config.TOKEN_NAME, '', expires=0)
    return response
