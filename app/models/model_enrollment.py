from . import db

class Enrollment(db.Model):
    __tablename__ = 'enrollment' 

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), primary_key=True)

    student = db.relationship('User', backref='enrollments', foreign_keys=[user_id])

    class_ = db.relationship('Class', backref=db.backref('enrollments', cascade="all, delete-orphan"), foreign_keys=[class_id])
