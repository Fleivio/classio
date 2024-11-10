from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)

    @staticmethod
    def create_password_hash(password):
        return generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hash_password, password)