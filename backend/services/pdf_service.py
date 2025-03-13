import fitz  # PyMuPDF
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

def pdf_to_text(pdf_path):
    """PDF dosyasını metne çevirir."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    return text

def extract_keywords(text, max_keywords=5):
    
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    words = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN", "ADJ"] and not token.is_stop]
    
    tfidf = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")  
    tfidf_matrix = tfidf.fit_transform([" ".join(words)])
    feature_names = tfidf.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    
    
    sorted_keywords = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
    keywords = [kw[0] for kw in sorted_keywords[:max_keywords]]
    
    return ", ".join(keywords)



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
    #     anonymized_fullpath = os.path.join(ANONYMIZED_FOLDER, anonymized_filename)

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