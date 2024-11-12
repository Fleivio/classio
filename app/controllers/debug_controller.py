from flask import request, jsonify
from app.models import User, Token
from app.models import db

class DebugController:
    @staticmethod
    def test():
        print('debug: test')
        a = request.form.get('a')
        print(a)
        return jsonify({"message": "Success"})

    
    @staticmethod
    def get_all_users():
        user = User.query.all()
        users = [{"id": u.user_id, "username": u.username, "email": u.email} for u in user]
        return jsonify(users)
    
    @staticmethod
    def get_user_by_id(id):
        user = User.query.filter_by(id=id).first()
        return user

    def add_user(self   ):
        print('debug: adding new user')
        print (request.json)

        json = request.json


        username = json['username']
        email = json['email']
        password = json['password']

        if not username or not email or not password:
            return jsonify({"message": "Missing parameters"}), 400

        user = User(username=username, email=email, hash_password=User.create_password_hash(password))

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User added successfully"})

    @staticmethod
    def login():
        print("debug: login")
        email = request.json['email'] 
        password = request.json['password']

        user = User.query.filter_by(email=email).first()
        # print(user)
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciais inválidas'}), 401

        return jsonify({"message": "Login successful"})

    @staticmethod
    def gen_token():
        email = request.json['email']
        password = request.json['password']
        
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({"message": "User not found"})
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciais inválidas'}), 401

        token = Token.generate_token(user)
        return jsonify({"token": token.token})
