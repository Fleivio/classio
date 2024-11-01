from flask import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

tk_name = 'classio_token'

def is_logged():
    token = request.cookies.get(tk_name)
    if token:
        # adicionar verificação da validade do token
        return True
    return False

@app.route("/")
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
    
@app.get("/login")
def login_get():
    if is_logged():
        return redirect("/")
    return render_template("login.jinja")

@app.post("/login")
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
    
@app.get("/signup")
def signup_get():
    if is_logged():
        return redirect("/")
    return render_template("sign_up.jinja")

@app.post("/signup")
def signup_post():
    #cria a conta
    response = make_response(redirect("/"))
    response.set_cookie(tk_name, 'default_token')
    return response

@app.route('/logout')
def logout():
    response = make_response(redirect("/"))
    response.set_cookie(tk_name, '', expires=0)
    return response

@app.get('/class')
def class_screen():
    if is_logged():
        class_id = request.args.get('class_id')
        # adicionar verificação da validade do acesso à turma
        # separar as rotas do aluno e do professor

        class_data = {
            'class_id': 'CLASS_TEST_ID',
            'name': 'Turma de Teste',
            'description': 'Turma de Teste',
            'professor': ['Marsio', 'Pedro'],
            'students': ['Carlos', 'Frederico'],
            'lessons' : [
                { 'name': 'Aula 1', 'id' : '1'},
                { 'name': 'Aula 2', 'id' : '2'},
                ]
            }
        
        return render_template("class_professor.jinja", class_data=class_data)
    else:
        return redirect("/")
    
@app.get('/class/stats')
def class_stats():
    if is_logged():
        class_id = request.args.get('class_id')
        # adicionar verificação da validade do acesso à turma como professor

        class_data = {
            'class_id': '1',
            'name': 'Turma de Teste',
            'description': 'Turma de Teste',
            'professor': ['Marsio', 'Pedro'],
            'students': ['Carlos', 'Frederico'],
            'lessons' : [
                { 'name': 'Aula 1', 'id' : '1'},
                { 'name': 'Aula 2', 'id' : '2'},
                ]
            }
        # adicionar verificação da validade do acesso à turma
        return render_template("class_stats.jinja", class_data=class_data)
    else:
        return redirect("/")

@app.get('/lesson')
def lesson_screen():
    if is_logged():
        lesson_id = request.args.get('lesson_id')
        # adicionar verificação da validade do acesso à aula

        lesson_data = {
            'lesson_id': '1',
            'name': 'Aula 1',
            'description': 'Aula de Teste',
            'content': 'Conteúdo da Aula',
            'class_id': 'CLASS_TEST_ID'
            }
        
        return render_template("lesson.jinja", lesson_data=lesson_data)
    else:
        return redirect("/")
