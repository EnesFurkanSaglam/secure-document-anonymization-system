from datetime import datetime
from models import db,User,Article,ArticleAssignment,Review,Log
from config import PUBLISHED_FOLDER
import os
from services.pdf_service import PdfService
import shutil

class ReviewerService:
    
    @staticmethod
    def list_assigned_articles_service(email):
        if not email or "@" not in email:
            return {"error" : "Invalid email address"}
        
        reviewer = User.query.filter_by(email=email, role="reviewer").first()
    
        if not reviewer:
            return {"error" : "Revewer not found"}
    
        assignments = ArticleAssignment.query.filter_by(reviewer_id=reviewer.id).all()
    
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
    def submit_review_service(email, tracking_code, review_text, is_final=False):
        if not email or not tracking_code or not review_text:
            return {"error": "Missing value"}, 400

        reviewer = User.query.filter_by(email=email, role="reviewer").first()
        if not reviewer:
            return {"error": "Reviewer not found"}, 404

        article = Article.query.filter_by(tracking_code=tracking_code).first()
        if not article:
            return {"error": "Article not found."}, 404
        
        article.status = "reviewed_and_send_back"
        db.session.add(article)
        db.session.commit()

        assignment = ArticleAssignment.query.filter_by(
            article_id=article.id, 
            reviewer_id=reviewer.id, 
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
        
        PdfService.merge_and_save_pdf(review_text,article)
        
        return {
            "message": "Review saved",
            "review_id": new_review.id,
            "is_final": is_final,
            "review_pdf_path": "null şimdilik" 
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
                "updated_at": rev.updated_at.isoformat() if rev.updated_at else None,
                "role" : rev.role,
                "interests" : rev.interests
            })

        return {"reviewers": results}, 200,
    
    @staticmethod
    def publish_article_service(article_id, reviewer_id=None):
   
        article = Article.query.get(article_id)
        if not article:
            return {"error": "Article not found."}, 404

        
        if not article.original_pdf_path or not os.path.exists(article.original_pdf_path):
            return {"error": "Review PDF not found or missing. Can't publish."}, 400

      

       
        base_filename = os.path.basename(article.original_pdf_path)
        published_path = os.path.join(PUBLISHED_FOLDER, base_filename)

       
        shutil.copy(article.original_pdf_path, published_path)

    
        article.published_pdf_path = published_path
        article.status = "published"
        db.session.commit()

      
        new_log = Log(
            article_id=article.id,
            user_id=reviewer_id, 
            action="article_published"
        )
        db.session.add(new_log)
        db.session.commit()

        return {
            "message": "Article has been published successfully.",
            "published_pdf_path": published_path
        }, 200