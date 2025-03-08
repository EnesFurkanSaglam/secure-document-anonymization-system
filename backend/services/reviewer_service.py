from datetime import datetime
from models import db,User,Article,ArticleAssignment,Review,Log

class ReviewerService:
    
    @staticmethod
    def list_assigned_articles_service(email):
        if not email or "@" not in email:
            return {"error" : "Invalid email address"}
        
        reviewer = User.query.filter_by(email=email, role="reviewer").first()
    
        if not reviewer:
            return {"error" : "Revewer nnot found"}
    
        assignments = ArticleAssignment.query.filter_by(reviewer_id=reviewer.id, active=True).all()
    
        results = []
    
        for assign in assignments:
            article = assign.article
        
            results.append({
                "assignment_id": assign.id,
                "article_id": article.id,
                "tracking_code": article.tracking_code,
                "anonymized_pdf_path": article.anonymized_pdf_path,
                "status": article.status,
                "assigned_at": assign.assigned_at.isoformat() if assign.assigned_at else None
            })

        return {"assigned_articles": results}, 200

    @staticmethod
    def submit_review_service(email,tracking_code,review_text,is_final=False):
        if not email or not tracking_code or not review_text:
            return {"error": "Missing value"}
    
        reviewer = User.query.filter_by(email=email, role="reviewer").first()
    
        if not reviewer:
            return {"error" : "Author not found"},404
    
    
        article = Article.query.filter_by(tracking_code=tracking_code).first()
        if not article:
            return {"error": "Article not found."}, 404
    
        assignment = ArticleAssignment.query.filter_by(
            article_id=article.id, 
            reviewer_id=reviewer.id, 
            active=True
        ).first()
    
        if not assignment:
            return {"error": "This article has not been assigned to this referee or the assignment is not active."}, 400

    
        new_review = Review(
            assignment_id=assignment.id,
            review_text=review_text,
            is_final=is_final
        )
        db.session.add(new_review)
        db.session.commit()

    
        new_log = Log(
            article_id=article.id,
            user_id=reviewer.id,
            action="review_submitted"
        )
        db.session.add(new_log)
        db.session.commit()

        return {
            "message": "Review saved",
            "review_id": new_review.id,
            "is_final": is_final
        }, 200
    
    @staticmethod    
    def list_all_reviewers_service():
        reviewers = User.query.filter_by(role="reviewer").all()
        results = []
        for rev in reviewers:
            results.append({
                "id": rev.id,
                "email": rev.email,
                "created_at": rev.created_at.isoformat() if rev.created_at else None,
                "updated_at": rev.updated_at.isoformat() if rev.updated_at else None
            })

        return {"reviewers": results}, 200