from flask import *
from .user import is_logged
from app.models import User
from app.models import db

debug = Blueprint('debug', __name__)

@debug.route('/get_users', methods=['GET'])
def get_users():
    user = User.query.all()
    users = [{"id": u.id, "nome": u.nome, "email": u.email} for u in user]
    return jsonify(users)

@debug.route('/get_user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    return user

@debug.route('/add_user', methods=['POST'])
def add_user():

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    user = User(nome=nome, email=email, senha_hash=senha)

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User added successfully"})