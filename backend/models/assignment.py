from datetime import datetime
from . import db

class ArticleAssignment(db.Model):
    __tablename__ = 'article_assignments'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, default=True)

    article = db.relationship("Article", backref="assignments", lazy=True)
    reviewer = db.relationship("User", backref="review_assignments", lazy=True)

    def __repr__(self):
        return f"<ArticleAssignment article:{self.article_id} reviewer:{self.reviewer_id}>"
