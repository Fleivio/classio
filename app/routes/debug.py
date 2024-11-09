from flask import *
from .user import is_logged
from app.models.models import User

debug = Blueprint('debug', __name__)

# Rota GET para recuperar todos os usuários
@debug.route('/get_users', methods=['GET'])
def get_users():
    usuarios = User.query.all()  # Recupera todos os usuários do banco de dados
    usuarios_lista = [{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios]
    return jsonify(usuarios_lista)
