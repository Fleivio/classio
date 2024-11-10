from .db import db
import secrets
from datetime import datetime, timedelta, timezone

class Token(db.Model):
    __tablename__ = 'token'

    token_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    token = db.Column(db.String(128), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('tokens', lazy=True))

    @staticmethod
    def generate_token(user, validade_horas=1):
        token = secrets.token_urlsafe(64)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=validade_horas)
        new_token = Token(user_id=user.user_id, token=token, expires_at=expires_at)

        db.session.add(new_token)
        db.session.commit()
        return new_token
    
    # TODO delete expired tokens