from flask import *
from .user import is_logged
from app.models import User, Token
from app.models import db

debug = Blueprint('debug', __name__)

@debug.route('/get_users', methods=['GET'])
def get_users():
    user = User.query.all()
    users = [{"id": u.user_id, "username": u.username, "email": u.email} for u in user]
    return jsonify(users)

@debug.route('/get_user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    return user

@debug.route('/add_user', methods=['POST'])
def add_user():

    username = request.form.get('name')
    email = request.form.get('email')
    senha = request.form.get('password')

    if not username or not email or not senha:
        return jsonify({"message": "Missing parameters"}), 400

    user = User(username=username, email=email, hash_password=User.create_password_hash(senha))

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User added successfully"})

@debug.route('/debug_login', methods=['POST'])
def debug_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    return jsonify({"message": "Login successful"})

@debug.route('/gen_token', methods=['GET'])
def gen_token():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"message": "User not found"})
    if not user or not user.check_password(password):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    token = Token.generate_token(user)
    return jsonify({"token": token.token})
