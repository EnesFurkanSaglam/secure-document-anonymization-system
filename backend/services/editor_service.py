import os 
from datetime import datetime 
from models import db,User,Article,Review,Log,ArticleAssignment,Message
from config import ANONYMIZED_FOLDER
import uuid

class EditorService:
    
    @staticmethod
    def list_all_articles_service():
        articles = Article.query.all()
        results = []
        for art in articles:
            results.append({
                "id": art.id,
                "tracking_code": art.tracking_code,
                "author_id": art.author_id,
                "keywords": art.keywords,
                "original_pdf_path": art.original_pdf_path,
                "anonymized_pdf_path": art.anonymized_pdf_path,
                "status": art.status,
                "created_at": art.created_at.isoformat() if art.created_at else None
            })
        return {"articles": results}, 200
    
    @staticmethod
    def get_article_by_id_service(article_id):
    
        if not article_id:
            return {"error": "article_id is required."}, 400

        try:
            article_id_int = int(article_id)
        except ValueError:
            return {"error": "article_id must be an integer."}, 400

        article = Article.query.get(article_id_int)
        if not article:
            return {"error": "Article not found."}, 404

        
        article_data = {
            "id": article.id,
            "tracking_code": article.tracking_code,
            "author_id": article.author_id,
            "keywords": article.keywords,
            "original_pdf_path": article.original_pdf_path,
            "anonymized_pdf_path": article.anonymized_pdf_path,
            "status": article.status,
            "created_at": article.created_at.isoformat() if article.created_at else None,
            "updated_at": article.updated_at.isoformat() if article.updated_at else None
        }

        return {"article": article_data}, 200
    

    @staticmethod
    def get_logs_by_article_id_service(article_id):
    
        if not article_id:
            return {"error": "article_id is required."}, 400

        try:
            article_id_int = int(article_id)
        except ValueError:
            return {"error": "article_id must be an integer."}, 400

    
        article = Article.query.get(article_id_int)
        if not article:
            return {"error": "Article not found."}, 404

    
        logs = Log.query.filter_by(article_id=article.id).order_by(Log.timestamp.asc()).all()

        results = []
        for lg in logs:
            results.append({
                "id": lg.id,
                "article_id": lg.article_id,
                "user_id": lg.user_id,
                "action": lg.action,
                "timestamp": lg.timestamp.isoformat() if lg.timestamp else None
            })

        return {"logs": results}, 200


    @staticmethod
    def list_articles_by_status_service(status):
        articles = Article.query.filter_by(status=status).all()
        results = []
        for art in articles:
            results.append({
                "id": art.id,
                "tracking_code": art.tracking_code,
                "author_id": art.author_id,
                "keywords": art.keywords,
                "original_pdf_path": art.original_pdf_path,
                "anonymized_pdf_path": art.anonymized_pdf_path,
                "status": art.status,
            })
        return {"articles": results}, 200
    
    
    @staticmethod
    def list_article_reviews_service(tracking_code):
        article = Article.query.filter_by(tracking_code=tracking_code).first()
        if not article:
            return {"error": "Article not found"}, 404

        all_assignments = article.assignments
        reviews_data = []

        for asg in all_assignments:
            for rev in asg.reviews:
                reviews_data.append({
                    "review_id": rev.id,
                    "review_text": rev.review_text,
                    "review_pdf_path": rev.review_pdf_path, 
                    "submitted_at": rev.submitted_at.isoformat() if rev.submitted_at else None,
                    "is_final": rev.is_final,
                    "reviewer_id": asg.reviewer_id
                })

        return {"reviews": reviews_data}, 200


    @staticmethod
    def view_logs_service():
        logs = Log.query.order_by(Log.timestamp.asc()).all()
        results = []
        for lg in logs:
            results.append({
               "id": lg.id,
                "article_id": lg.article_id,
                "user_id": lg.user_id,
                "action": lg.action,
                "timestamp": lg.timestamp.isoformat() if lg.timestamp else None
            })
        return {"logs": results}, 200
    
    
    @staticmethod
    def list_article_messages_service(tracking_code):
        if not tracking_code:
            return {"error" : "tracking_code required"},400
        
        article = Article.query.filter_by(tracking_code=tracking_code).first()
        if not article:
            return {"error": "Article not found"},404
        
        msgs = Message.query.filter_by(article_id=article.id).order_by(Message.created_at.asc()).all()

        conversation = []
        for m in msgs:
            conversation.append({
            "message_id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "content": m.content,
            "created_at": m.created_at.isoformat() if m.created_at else None
        })

        return {"conversation": conversation}, 200
    
    @staticmethod
    def send_message_as_editor_service(tracking_code, content):
    
        if not tracking_code or not content:
            return {"error": "tracking_code and content required."}, 400

    
        editor = User.query.filter_by(role="editor").first()
        if not editor:
            return {"error": "Editor not found"}, 500

        article = Article.query.filter_by(tracking_code=tracking_code).first()
        if not article:
            return {"error": "Article not found"}, 404

    
        author = User.query.get(article.author_id)
        if not author:
            return {"error": "Author not found."}, 404

    
        msg = Message(
            sender_id=editor.id,
            receiver_id=author.id,
            article_id=article.id,
            content=content
        )
        db.session.add(msg)
        db.session.commit()

    
        log = Log(article_id=article.id, user_id=editor.id, action="editor_sent_message")
        db.session.add(log)
        db.session.commit()

        return {"message": "Message sent to author."}, 200
    
    
