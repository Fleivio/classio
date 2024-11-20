from . import db


class Question(db.Model):
    __tablename__ = "question"

    question_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)

    is_multiple_choice = db.Column(db.Boolean, nullable=False)

    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.lesson_id"), nullable=False)

    lesson = db.relationship("Lesson", backref=db.backref('questions', cascade="all, delete-orphan"), foreign_keys=[lesson_id])

    qs_answers = db.relationship("Answer", cascade="all, delete-orphan")


class Answer(db.Model):
    __tablename__ = "answer"

    answer_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.question_id"), nullable=False
    )

    question = db.relationship("Question", backref=db.backref("answers", cascade="all, delete-orphan"), foreign_keys=[question_id])
    student = db.relationship("User", backref="answers")


    def to_dict(self):
        return {
            "answer_id": self.answer_id,
            "answer": self.answer,
            "date_created": self.date_created,
            "user_id": self.user_id,
            "question_id": self.question_id,
        }