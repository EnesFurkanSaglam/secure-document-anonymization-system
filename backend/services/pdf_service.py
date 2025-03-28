import os
import io
import tempfile
import fitz
import spacy
import cv2
import numpy as np
from pdf2image import convert_from_path
from fpdf import FPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from models import db, Article, ArticleAssignment, Log, User,Review
from config import ANONYMIZED_FOLDER, REVIEWS_FOLDER
from services.encryption_service import EncryptionService

from services.anonim import (
    extract_text_from_pdf,
    find_first_person_name_and_extract_context,
    get_entities_ensemble,
    find_emails,
    censor_pdf
)

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
    def extract_keywords(text, max_keywords=15):
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
    def blur_pdf_faces(input_pdf_path, output_pdf_path):
        
        poppler_path = r"D:\\NS\\ca_Secure Document Anonymization System\\poppler-24.08.0\\Library\bin"
       
        pages = convert_from_path(input_pdf_path, dpi=300, poppler_path=poppler_path)
        face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(face_cascade_path)
        processed_image_paths = []

        for i, page in enumerate(pages):
            
            img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                face_roi = img[y:y+h, x:x+w]
                blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
                img[y:y+h, x:x+w] = blurred_face
            
            temp_img_path = os.path.join(tempfile.gettempdir(), f"temp_blur_page_{i}.jpg")
            cv2.imwrite(temp_img_path, img)
            processed_image_paths.append(temp_img_path)

        
        pdf = FPDF()
        for image in processed_image_paths:
            pdf.add_page()
            
            pdf.image(image, x=0, y=0, w=210, h=297)
        pdf.output(output_pdf_path, "F")
        
        for image in processed_image_paths:
            os.remove(image)

    @staticmethod
    def anonymize_and_assign(article_id, anonymize_names=False, anonymize_photos=False):
        article = Article.query.filter_by(id=article_id).first()
        if not article:
            return {"error": "Article not found"}, 404

        source_path = article.original_pdf_path
        if not source_path or not os.path.exists(source_path):
            return {"error": "Original PDF not found on server"}, 404

        base_filename = os.path.basename(source_path)
        destination_path = os.path.join(ANONYMIZED_FOLDER, base_filename)

        with open(source_path, "rb") as f:
            enc_data = f.read()
        dec_data = EncryptionService.decrypt_data(enc_data)

        
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(dec_data)
            tmp.flush()
            temp_path = tmp.name

       
        full_text = extract_text_from_pdf(temp_path)

        
        processed_pdf_path = temp_path

        
        if anonymize_names:
            first_person, extracted_text = find_first_person_name_and_extract_context(full_text)
            sensitive_entities = set()
            if extracted_text:
                sensitive_entities.update(get_entities_ensemble(extracted_text))
            emails = find_emails(full_text)
            if emails:
                sensitive_entities.update(emails)
            words_to_censor = list(sensitive_entities)
            redacted_pdf_path = os.path.join(tempfile.gettempdir(), f"redacted_{base_filename}")
            censor_pdf(temp_path, words_to_censor, redacted_pdf_path)
            processed_pdf_path = redacted_pdf_path

        
        final_plain_pdf_path = os.path.join(tempfile.gettempdir(), f"final_{base_filename}")
        if anonymize_photos:
            PdfService.blur_pdf_faces(processed_pdf_path, final_plain_pdf_path)
            processed_pdf_path = final_plain_pdf_path

        
        with open(processed_pdf_path, "rb") as f:
            final_plain_data = f.read()
        final_enc_data = EncryptionService.encrypt_data(final_plain_data)
        with open(destination_path, "wb") as f:
            f.write(final_enc_data)

        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if anonymize_names and os.path.exists(redacted_pdf_path):
            os.remove(redacted_pdf_path)
        if anonymize_photos and os.path.exists(final_plain_pdf_path):
            os.remove(final_plain_pdf_path)

        
        article.anonymized_pdf_path = destination_path
        article.status = "assigned"

        
        article_keywords = PdfService.extract_keywords(full_text, max_keywords=5)

        nlp = spacy.load("en_core_web_md")
        doc_keywords = nlp(article_keywords)
        doc_full = nlp(full_text)

        reviewers = User.query.filter_by(role="reviewer").all()
        if not reviewers:
            return {"error": "No reviewers found in the system"}, 404

        best_reviewer = None
        best_ensemble_score = -1

        for reviewer in reviewers:
            if not reviewer.interests:
                ensemble_score = 0.0
            else:
                reviewer_doc = nlp(reviewer.interests)
                score_keywords = doc_keywords.similarity(reviewer_doc)
                score_full = doc_full.similarity(reviewer_doc)
                ensemble_score = (score_keywords + score_full) / 2.0
            if ensemble_score > best_ensemble_score:
                best_ensemble_score = ensemble_score
                best_reviewer = reviewer

        if not best_reviewer:
            best_reviewer = reviewers[0]

        
        existing_assignments = ArticleAssignment.query.filter_by(article_id=article.id, active=True).all()
        for assignment in existing_assignments:
            associated_reviews = Review.query.filter_by(assignment_id=assignment.id).all()
            for review in associated_reviews:
                db.session.delete(review)
            db.session.delete(assignment)

        new_assignment = ArticleAssignment(
            article_id=article.id,
            reviewer_id=best_reviewer.id,
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
            user_id=best_reviewer.id,
            action="assigned_to_reviewer"
        )
        db.session.add(new_log_assign)

        db.session.commit()

        return {
            "message": f"Article anonymized and assigned to reviewer with id={best_reviewer.id}.",
            "assigned_reviewer_id": best_reviewer.id,
            "anonymized_path": destination_path,
            "article_keywords": article_keywords,
            "ensemble_similarity_score": best_ensemble_score
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
