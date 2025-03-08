import os 
from datetime import datetime 
from models import db,User,Article,Review,Log,ArticleAssignment

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
    def auto_assign_article_service(tracking_code):

        article = Article.query.filter_by(tracking_code=tracking_code).first()
        if not article:
            return {"error": "Article not found"}, 404

            if article.status == "assigned":
                return {"error": "Article already assigned."}, 400

    
        # article_keywords = parse_to_set(article.keywords)
        # if not article_keywords:
        #     return {"error": "Makale için anahtar kelime yok."}, 400

    
        reviewers = User.query.filter_by(role="reviewer").all()

        suitable_reviewer = None
        # for rev in reviewers:
        #     rev_interests = parse_to_set(rev.interests)
        #     if article_keywords & rev_interests:  # Kesişim boş değilse
        #         suitable_reviewer = rev
        #         break

        if not suitable_reviewer:
            return {"error": "No suitable referee found (no intersection)."}, 400

    
        new_assignment = ArticleAssignment(article_id=article.id, reviewer_id=suitable_reviewer.id)
        db.session.add(new_assignment)

        article.status = "assigned"
        db.session.commit()

        log = Log(article_id=article.id, user_id=suitable_reviewer.id, action="article_assigned_auto")
        db.session.add(log)
        db.session.commit()

        return {"message": f"Article {suitable_reviewer.email} assigned."}, 200

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


    #!nlp işleminden sonra düzeltiecek
    # @staticmethod
    # def revert_anonymized_sections_service(tracking_code):
    #     """
    #     Yazar bilgilerini geri getirme (placeholder).
    #     Proje isterinde "editör anonimleştirilen bilgilerin bazılarını geri yükleyebilir" deniyor.
    #     Şimdilik 'status' = "deanonimized" yapıp anonymized_pdf_path'i silmek gibi 
    #     bir mantık.
    #     """
    #     article = Article.query.filter_by(tracking_code=tracking_code).first()
    #     if not article:
    #         return {"error": "Makale bulunamadı."}, 404

    #     article.anonymized_pdf_path = None
    #     article.status = "deanonimized"
    #     db.session.commit()

    #     # Log
    #     log = Log(article_id=article.id, user_id=None, action="article_deanonimized")
    #     db.session.add(log)
    #     db.session.commit()

    #     return {"message": "Anonymized sections reverted (placeholder)."}, 200

    # #!nlp işleminden sonra düzeltiecek
    # @staticmethod
    # def parse_to_set(text):
    #     """
    #     "AI, Deep Learning , NLP" -> {"ai", "deep learning", "nlp"}
    #     Basit bir virgülle ayrılmış alan parse etme.
    #     """
    #     if not text:
    #         return set()
    #     return set([kw.strip().lower() for kw in text.split(",") if kw.strip()])

    # #!nlp işleminden sonra düzeltiecek
    # @staticmethod
    # def anonymize_article_service(tracking_code, options=None):
    #     """
    #     Placeholder anonimleştirme fonksiyonu.
    #       - 'tracking_code': Hangi makaleyi işleyeceğiz?
    #       - 'options': Yazar adı, kurum bilgisi vs. gibi seçilecek alanlar (şimdilik kullanılmıyor).
    #     İLERİDE: PDF içindeki yazar/kurum bilgileri regex, NER vs. ile maskelenip
    #     yeni bir anonymized_pdf_path oluşturulabilir.
    #     """
    #     article = Article.query.filter_by(tracking_code=tracking_code).first()
    #     if not article:
    #         return {"error": "Makale bulunamadı."}, 404

    #     anonymized_filename = f"anon_{tracking_code}.pdf"
    #     anonymized_fullpath = os.path.join("uploads", anonymized_filename)

    #     # Örnek: Orijinal PDF'i kopyalamak / manipüle etmek istiyorsan
    #     # copy_or_anonymize_pdf(article.original_pdf_path, anonymized_fullpath)
    #     # Şimdilik sadece placeholder

    #     article.anonymized_pdf_path = anonymized_fullpath
    #     article.status = "anonymized"
    #     db.session.commit()

    #     # Log
    #     log = Log(article_id=article.id, user_id=None, action="article_anonymized")
    #     db.session.add(log)
    #     db.session.commit()

    #     return {
    #         "message": "Makale anonimleştirildi (placeholder).",
    #         "anonymized_pdf_path": anonymized_fullpath
    #     }, 200