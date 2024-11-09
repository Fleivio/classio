from flask import * 

tk_name = 'classio_token'

user = Blueprint('user', __name__)

def is_logged():
    token = request.cookies.get(tk_name)
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
    username = request.form["username"]
    password = request.form["password"]
    if (username == "eduardo"):
        # adicionar verificação de senha e email
        response = make_response(redirect("/"))
        response.set_cookie(tk_name, 'default_token')
        return response
    else:
        flash('Email inválido. Tente novamente.')
        return redirect('/login')
    
@user.get("/signup")
def signup_get():
    if is_logged():
        return redirect("/")
    return render_template("sign_up.jinja")

@user.post("/signup")
def signup_post():
    #cria a conta
    response = make_response(redirect("/"))
    response.set_cookie(tk_name, 'default_token')
    return response

@user.route('/logout')
def logout():
    response = make_response(redirect("/"))
    response.set_cookie(tk_name, '', expires=0)
    return response
