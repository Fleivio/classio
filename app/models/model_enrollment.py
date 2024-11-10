from .db import db

class Enrollment(db.Model):
    __tablename__ = 'enrollment' 

    student_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), primary_key=True)

    student = db.relationship('User', backref='enrollments', foreign_keys=[student_id])
    class_ = db.relationship('Class', backref='enrollments', foreign_keys=[class_id])
