from flask import *
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index_screen():
    return render_template("index.jinja")

@app.get("/login")
def login_get():
    return render_template("login.jinja")

@app.post("/login")
def login_post():
    return "<p>You are now logged in.</p>"