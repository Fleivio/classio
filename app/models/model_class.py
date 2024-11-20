from . import db

class Class(db.Model):
    __tablename__ = 'class'

    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(64), nullable=False)
    class_description = db.Column(db.String(256), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    professor = db.relationship('User', backref=db.backref('classes', lazy=True))

    # cl_lessons = db.relationship('Lesson', back_populates='class_', cascade="all, delete-orphan")
    # cl_enrollments = db.relationship('Enrollment', back_populates='class_', cascade="all, delete-orphan")
    # cl_threads = db.relationship('Thread', back_populates='class_', cascade="all, delete-orphan")

    def usr_has_access_professor(id, token):
        if not token:
            return False
        if not id:
            return False
        cl = Class.query.filter_by(class_id=id).first()
        return token.user_id == cl.professor_id
    
    def usr_has_access_student(id, token):
        if not token:
            return False
        cl = Class.query.filter_by(class_id=id).first()
        return token.user_id in map(lambda x: x.user_id, cl.enrollments)
    
    def to_dict(self):
        return {
            "class_name": self.class_name,
            "class_description": self.class_description,
            "class_id": str(self.class_id),
            "professor_id": str(self.professor_id),
            "lessons": list(map(lambda x: {
                "lesson_id": str(x.lesson_id),
                "lesson_title": x.title,
            }, self.lessons))
        }
