from . import db


class StatQuestion(db.Model):
    __tablename__ = "stat_question"

    st_question_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"), nullable=False)

    st_ans = db.relationship('StAnswer', cascade="all, delete-orphan")
    st_class = db.relationship('Class', backref=db.backref('stat_questions', cascade="all, delete-orphan"), foreign_keys=[class_id])
    
    def get_avg(self):
        return sum([ans.answer for ans in self.st_ans]) / len(self.st_ans)
    
class StAnswer(db.Model):
    __tablename__ = "stat_answer"

    answer_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("stat_question.st_question_id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.lesson_id"), nullable=False)

    student = db.relationship("User", backref="st_answers")
    question = db.relationship("StatQuestion", backref=db.backref("st_answers", cascade="all, delete-orphan"), foreign_keys=[question_id])

    