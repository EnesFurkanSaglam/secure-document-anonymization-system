from datetime import datetime
from . import db

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tracking_code = db.Column(db.String(50), unique=True, nullable=False)

    keywords = db.Column(db.String(255), nullable=True)

    original_pdf_path = db.Column(db.String(255), nullable=True)
    anonymized_pdf_path = db.Column(db.String(255), nullable=True)
    published_pdf_path = db.Column(db.String(255), nullable=True)
    review_pdf_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default="uploaded")  # "uploaded", "assigned", ...
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship("User", backref="articles", lazy=True)

    def __repr__(self):
        return f"<Article {self.id} - Tracking:{self.tracking_code}>"
