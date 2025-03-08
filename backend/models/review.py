from datetime import datetime
from . import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('article_assignments.id'), nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_final = db.Column(db.Boolean, default=False)  # final mi?

    assignment = db.relationship("ArticleAssignment", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.id}>"