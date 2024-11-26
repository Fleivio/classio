from . import db

class Thread(db.Model):
    __tablename__ = "thread"

    thread_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"), nullable=False)

    user = db.relationship("User", backref="threads")
    class_ = db.relationship('Class', backref=db.backref('threads', cascade="all, delete-orphan"), foreign_keys=[class_id])

class Thread_Response(db.Model):
    __tablename__ = "thread_response"

    response_id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey("thread.thread_id"), nullable=False)

    user = db.relationship("User", backref="responses")
    thread = db.relationship("Thread", backref=db.backref("responses", cascade="all, delete-orphan"), foreign_keys=[thread_id])


