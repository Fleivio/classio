from flask import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index_screen():
    logged = False
    if logged:
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
        return redirect("/")
    else:
        flash('Email inválido. Tente novamente.')
        return redirect('/login')
        