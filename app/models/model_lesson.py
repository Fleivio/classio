from . import db

class Lesson(db.Model):
    __tablename__ = 'lesson'

    lesson_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), nullable=False) 

    class_ = db.relationship('Class', backref='lessons')

    def to_dict(self):
        return {
            "lesson_id": str(self.lesson_id),
            "title": self.title,
            "description": self.description,
            "class_id": str(self.class_id)
        }