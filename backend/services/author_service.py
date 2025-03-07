import os 
import uuid
from werkzeug.utils import secure_filename
from models import db, User, Article, Message, Log


UPLOAD_FOLDER = "uploads"

def generate_tracking_code():
    return str(uuid.uuid4())[:8]

def get_or_create_author_by_email(email):
    author = User.query.filter_by(email = email,role="author").first()
    
    if not author:
        author = User(email=email,role="author")
        db.session.add(author)
        db.session.commit()
        
    return author


def upload_article_service(email,pdf_file):
    if not email or "@" not in email:
        return {"error" : "A valid email address must be entered."},400
    
    if not pdf_file or pdf_file.filename == "":
        return {"error":"PDF file could not be loaded or invalid file name"},400
    
    author = get_or_create_author_by_email(email)
    
    filename = secure_filename(pdf_file.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER,filename)
    pdf_file.save(pdf_path)
    
    tracking_code = generate_tracking_code()
    
    
    new_article = Article(
        author_id = author.id,
        tracking_code = tracking_code,
        original_pdf_path = pdf_path,
        status = "uploaded"
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    log = Log(article_id = new_article.id,user_id=author.id,action="article_uploaded")
    db.session.add(log)
    db.session.commit()
    
    return{
        "message": "Article uploaded succesfully",
        "tracking_code" : tracking_code
    },200
    
    
def send_message_service(email,tracking_code,content):
    if not email or not tracking_code or not content:
        return {"error" : "Missing value"},400
    
    author = User.query.filter_by(email = email, role="author").first()
    if not author:
        return{"error" : "Author could not find"},404
    
    article = Article.query.filter_by(tracking_code=tracking_code, author_id=author.id).first()
    if not article:
        return {"error": "The article was not found or does not belong to you."}, 404
    
    
    #! Editör (tek editör varsayımı)
    editor_user = User.query.filter_by(role="editor").first()
    if not editor_user:
        return {"error": "Editor could not finnd."}, 500
    
    
    msg = Message(
        sender_id = author.id,
        receiver_id = editor_user.id,
        article_id = article.id,
        content = content
    )
    
    db.session(msg)
    db.session.commit()
    
    log = Log(article_id=article.id, user_id=author.id, action="author_sent_message")
    db.session.add(log)
    db.session.commit()
    
    return {"message": "Message forwarded to editor."}, 200


def check_status_service(email, tracking_code):
    """Yazarın makale durumunu sorgulaması."""
    if not email or not tracking_code:
        return {"error": "tracking_code ve email gerekli."}, 400

    author = User.query.filter_by(email=email, role="author").first()
    if not author:
        return {"error": "Yazar bulunamadı."}, 404

    article = Article.query.filter_by(tracking_code=tracking_code, author_id=author.id).first()
    if not article:
        return {"error": "Makale bulunamadı veya size ait değil."}, 404

    #! Burada review / assignment gibi ek bilgiler döndürebilirsin
    response_data = {
        "tracking_code": article.tracking_code,
        "status": article.status,
        "message": "Şu anki durum: " + article.status
    }

    return response_data, 200

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
        return {"error": "The article was not found or does not belong to you"}, 404

   
    filename = secure_filename(pdf_file.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_file.save(pdf_path)

    
    article.original_pdf_path = pdf_path
    article.status = "reuploaded"
    db.session.commit()

    
    log = Log(article_id=article.id, user_id=author.id, action="article_reuploaded")
    db.session.add(log)
    db.session.commit()

    return {
        "message": "Article updated (revision uploaded).",
        "new_path": pdf_path
    }, 200






    
    
    
    
    
        
    

    
    
