from flask import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index_screen():
    token = request.cookies.get('auth_token')
    if token:
        # adicionar verificação da validade do token
        return render_template("index_logged.jinja")
    else:
        return render_template("index.jinja")
    
@app.get("/login")
def login_get():
    return render_template("login.jinja")

@app.post("/login")
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if (username == "eduardo"):
        # adicionar verificação de senha e email
        response = make_response(redirect(url_for('index_screen')))
        response.set_cookie('auth_token', 'default_token')
        return response
    else:
        flash('Email inválido. Tente novamente.')
        return redirect('/login')

@app.route('/logout')
def logout():
    # Remove o cookie de autenticação
    response = make_response(redirect(url_for('index_screen')))
    response.set_cookie('auth_token', '', expires=0)
    return response