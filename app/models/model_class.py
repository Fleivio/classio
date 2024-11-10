from . import db

class Class(db.Model):
    __tablename__ = 'class'

    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(64), nullable=False)
    class_description = db.Column(db.String(256), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    professor = db.relationship('User', backref=db.backref('classes', lazy=True))

    