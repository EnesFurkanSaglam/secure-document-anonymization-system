from datetime import datetime
from . import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship("User", foreign_keys=[sender_id], backref="messages_sent", lazy=True)
    receiver = db.relationship("User", foreign_keys=[receiver_id], backref="messages_received", lazy=True)
    article = db.relationship("Article", backref="messages", lazy=True)

    def __repr__(self):
        return f"<Message from:{self.sender_id} to:{self.receiver_id}>"
