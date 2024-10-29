from flask import *

app = Flask(__name__)

@app.route("/")
def index_screen():
    return """
    <h1>Classio</h1>
    <p>Bem-vindo à página inicial.</p>
    <p>Acesse a página de <a href="/login">Login</a>.</p>
    """

@app.route("/login")
def login_screen():
    password = request.args.get('password')
    print(password)
    return "<h1>Login</h1>"

@app.route("/statistics")
def statistics_screen():
    return "<h1>Statistics</h1>"

@app.route("/class")
def class_screen():
    return "<h1>Class</h1>"
