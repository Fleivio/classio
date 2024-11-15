from . import db

class Question(db.Model):
    __tablename__ = 'question'

    question_id = db.Colum(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)

    is_multiple_choice = db.Column(db.Boolean, nullable=False)

    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'), nullable=False)

    lesson = db.relationship('Lesson', backref='questions')

class Option(db.Model):
    __tablename__ = 'option'

    option_id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(128), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)

    question = db.relationship('Question', backref='options')

class Answer(db.Model):
    __tablename__ = 'answer'

    answer_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)

    question = db.relationship('Question', backref='answers')
    student = db.relationship('Student', backref='answers')

class OptionAnswer(db.Model):
    __tablename__ = 'option_answer'

    option_answer_id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.answer_id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.option_id'), nullable=False)

    answer = db.relationship('Answer', backref='option_answers')
    option = db.relationship('Option', backref='option_answers')