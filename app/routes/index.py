from flask import * 
from app.config import Config
from app.models import Token

index = Blueprint('index', __name__)

def has_active_token():
    cookie_token = request.cookies.get(Config.TOKEN_NAME)
    token = Token.query.filter_by(token=cookie_token).first()

    if token and not token.expired():
        return True
    return False

@index.route("/")
def index_screen():
    if has_active_token():
        return redirect("/home")
    else:
        return render_template("index.jinja")
    
@index.get("/login")
def login_get():
    if has_active_token():
        return redirect("/")
    return render_template("login.jinja")

@index.get("/signup")
def signup_get():
    if has_active_token():
        return redirect("/")
    return render_template("sign_up.jinja")