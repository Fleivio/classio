from app.config import Config
from app.models import Token, User, db
from app.routes.index import get_active_token
from flask import Blueprint, make_response, redirect, request

user = Blueprint('user', __name__)

@user.post("/login")
def login():
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

@user.get('/logout')
def logout():
    token = get_active_token()

    if token:
        db.session.delete(token)
        db.session.commit()

    response = make_response(redirect("/"))
    response.set_cookie(Config.TOKEN_NAME, '', expires=0)
    return response

@user.post("/create")
def create():
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
