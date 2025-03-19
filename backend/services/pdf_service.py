import os
import shutil
import io
import tempfile
import fitz
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from models import db, Article, ArticleAssignment, Log
from config import ANONYMIZED_FOLDER, REVIEWS_FOLDER
from services.encryption_service import EncryptionService

class PdfService:

    @staticmethod
    def pdf_to_text(pdf_path):
        
        with open(pdf_path, "rb") as f:
            encrypted_data = f.read()

        
        decrypted_data = EncryptionService.decrypt_data(encrypted_data)

        
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(decrypted_data)
            tmp.flush()
            temp_path = tmp.name

        
        doc = fitz.open(temp_path)
        text_chunks = []
        for page in doc:
            text_chunks.append(page.get_text())
        doc.close()

        
        os.remove(temp_path)

       
        return "\n".join(text_chunks)

    @staticmethod
    def extract_keywords(text, max_keywords=5):
 
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)

        words = [
            token.text.lower()
            for token in doc
            if token.pos_ in ["NOUN", "PROPN", "ADJ"] and not token.is_stop
        ]

        tfidf = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        tfidf_matrix = tfidf.fit_transform([" ".join(words)])
        feature_names = tfidf.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]

        sorted_keywords = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
        keywords = [kw[0] for kw in sorted_keywords[:max_keywords]]
        return ", ".join(keywords)

    @staticmethod
    def anonymize_and_assign(article_id):

        article = Article.query.filter_by(id=article_id).first()
        if not article:
            return {"error": "Article not found"}, 404

        source_path = article.original_pdf_path
        base_filename = os.path.basename(source_path)
        destination_path = os.path.join(ANONYMIZED_FOLDER, base_filename)

        with open(source_path, "rb") as f:
            enc_data = f.read()

        
        dec_data = EncryptionService.decrypt_data(enc_data)

        new_enc_data = EncryptionService.encrypt_data(dec_data)

        
        with open(destination_path, "wb") as f:
            f.write(new_enc_data)

       
        article.anonymized_pdf_path = destination_path
        article.status = "assigned"

        
        reviewer_id = 2 
        new_assignment = ArticleAssignment(
            article_id=article.id,
            reviewer_id=reviewer_id,
            active=True
        )
        db.session.add(new_assignment)

        new_log_anon = Log(
            article_id=article.id,
            user_id=None,
            action="article_anonymized"
        )
        db.session.add(new_log_anon)

        new_log_assign = Log(
            article_id=article.id,
            user_id=reviewer_id,
            action="assigned_to_reviewer"
        )
        db.session.add(new_log_assign)

        db.session.commit()

        return {
            "message": "Article anonymized and assigned to reviewer with id=2.",
            "assigned_reviewer_id": reviewer_id,
            "anonymized_path": destination_path
        }, 200

    @staticmethod
    def merge_and_save_pdf(review_text, article):


        input_path = article.original_pdf_path
        output_filename = os.path.basename(input_path)
        output_path = os.path.join(REVIEWS_FOLDER, output_filename)

        review_text = "Reviewer Notes: " + review_text
        os.makedirs(REVIEWS_FOLDER, exist_ok=True)

        
        with open(input_path, "rb") as file:
            enc_data = file.read()
        dec_data = EncryptionService.decrypt_data(enc_data)

        
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_in:
            tmp_in.write(dec_data)
            tmp_in.flush()
            tmp_in_path = tmp_in.name

        input_pdf = PdfReader(tmp_in_path)
        output_pdf = PdfWriter()

        
        for page in input_pdf.pages:
            output_pdf.add_page(page)

        
        if input_pdf.pages:
            last_page = input_pdf.pages[-1]
            page_width = float(last_page.mediabox.width)
            page_height = float(last_page.mediabox.height)
        else:
            page_width, page_height = (595.2, 841.8)  

        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        c.drawString(50, page_height - 50, review_text)
        c.showPage()
        c.save()

        packet.seek(0)
        new_page_pdf = PdfReader(packet)
        new_page = new_page_pdf.pages[0]
        output_pdf.add_page(new_page)

        
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_out:
            output_pdf.write(tmp_out)
            tmp_out.flush()
            tmp_out_path = tmp_out.name

        
        with open(tmp_out_path, "rb") as tmp_out_file:
            merged_plain_data = tmp_out_file.read()

        merged_enc_data = EncryptionService.encrypt_data(merged_plain_data)

        with open(output_path, "wb") as final_file:
            final_file.write(merged_enc_data)

        
        article.review_pdf_path = output_path
        db.session.add(article)
        db.session.commit()

        
        os.remove(tmp_in_path)
        os.remove(tmp_out_path)

