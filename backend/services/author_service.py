import os 
import uuid
from werkzeug.utils import secure_filename
from models import db, User, Article, Message, Log
from config import ORIGINAL_FOLDER


UPLOAD_FOLDER = "uploads"

class AuthorService:
    @staticmethod
    def generate_tracking_code():
        return str(uuid.uuid4())[:8]

    @staticmethod
    def get_or_create_author_by_email(email):
        author = User.query.filter_by(email=email, role="author").first()
        
        if not author:
            author = User(email=email, role="author")
            db.session.add(author)
            db.session.commit()
        
        return author

    @staticmethod
    def upload_article_service(email, pdf_file):
        if not email or "@" not in email:
            return {"error": "A valid email address must be entered."}, 400
    
        if not pdf_file or pdf_file.filename == "":
            return {"error": "PDF file could not be loaded or invalid file name"}, 400
    
        author = AuthorService.get_or_create_author_by_email(email)
    
        
        original_filename = secure_filename(pdf_file.filename)
        
        unique_suffix = uuid.uuid4().hex
        filename = f"{unique_suffix}_{original_filename}"
    
        pdf_path = os.path.join(ORIGINAL_FOLDER, filename)
        pdf_file.save(pdf_path)
    
        tracking_code = AuthorService.generate_tracking_code()
    
        new_article = Article(
            author_id=author.id,
            tracking_code=tracking_code,
            original_pdf_path=pdf_path,
            status="uploaded"
        )
    
        db.session.add(new_article)
        db.session.commit()
    
        log = Log(article_id=new_article.id, user_id=author.id, action="article_uploaded")
        db.session.add(log)
        db.session.commit()
    
        return {"message": "Article uploaded successfully", "tracking_code": tracking_code}, 200
    
    
    @staticmethod
    def check_status_service(email, tracking_code):
        if not email or not tracking_code:
            return {"error": "Tracking code and email are required."}, 400
        
        author = User.query.filter_by(email=email, role="author").first()
        if not author:
            return {"error": "Author not found"}, 404
        
        article = Article.query.filter_by(tracking_code=tracking_code, author_id=author.id).first()
        if not article:
            return {"error": "The article was not found or does not belong to you."}, 404
        
        return {"tracking_code": article.tracking_code, "status": article.status, "message": "Current status: " + article.status}, 200



    @staticmethod
    def reupload_article_service(email, tracking_code, pdf_file):
        if not email or "@" not in email or not tracking_code:
            return {"error": "Valid email and tracking_code required."}, 400

        if not pdf_file or pdf_file.filename == "":
            return {"error": "PDF file not loaded or invalid file name."}, 400

        author = User.query.filter_by(email=email, role="author").first()
        if not author:
            return {"error": "Author not found."}, 404

        article = Article.query.filter_by(tracking_code=tracking_code, author_id=author.id).first()
        if not article:
            return {"error": "The article was not found or does not belong to you."}, 404

    
        original_filename = secure_filename(pdf_file.filename)
    
        unique_suffix = uuid.uuid4().hex
        filename = f"{unique_suffix}_{original_filename}"

        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        pdf_file.save(pdf_path)

        article.original_pdf_path = pdf_path
        article.status = "reuploaded"
        db.session.commit()

        log = Log(article_id=article.id, user_id=author.id, action="article_reuploaded")
        db.session.add(log)
        db.session.commit()

        return {"message": "Article updated (revision uploaded).", "new_path": pdf_path}, 200


    @staticmethod
    def list_conversation_service(email,tracking_code):
        
        author = User.query.filter_by(email=email,role="author").first()
        if not author:
            return{"error" : "Author not found"},404
        
        article = Article.query.filter_by(tracking_code=tracking_code, author_id=author.id).first()
        if not article:
            return {"error": "Article not found or not yours."}, 404
        
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
    def send_message_service(email, tracking_code, content):
        if not email or not tracking_code or not content:
            return {"error": "Missing value"}, 400
        
        author = User.query.filter_by(email=email, role="author").first()
        if not author:
            return {"error": "Author could not be found"}, 404
        
        article = Article.query.filter_by(tracking_code=tracking_code, author_id=author.id).first()
        if not article:
            return {"error": "The article was not found or does not belong to you."}, 404
        
        editor_user = User.query.filter_by(role="editor").first()
        if not editor_user:
            return {"error": "Editor not found."}, 500
        
        msg = Message(
            sender_id=author.id,
            receiver_id=editor_user.id,
            article_id=article.id,
            content=content
        )
        
        db.session.add(msg)
        db.session.commit()
        
        log = Log(article_id=article.id, user_id=author.id, action="author_sent_message")
        db.session.add(log)
        db.session.commit()
        
        return {"message": "Message forwarded to editor."}, 200
    
    @staticmethod
    def nlp_extract_keywords(pdf_path):
        return "AI, Deep Learning"
