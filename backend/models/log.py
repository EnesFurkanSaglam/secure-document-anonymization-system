from datetime import datetime
from . import db

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)  # "article_uploaded", "assigned_to_reviewer".
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    article = db.relationship("Article", backref="logs", lazy=True)
    user = db.relationship("User", backref="logs", lazy=True)

    def __repr__(self):
        return f"<Log article:{self.article_id}, user:{self.user_id}, action:{self.action}>"
