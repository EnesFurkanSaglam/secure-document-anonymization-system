import fitz
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from models import db, Article,ArticleAssignment,Log
from config import ANONYMIZED_FOLDER,REVIEWS_FOLDER
import os
import shutil
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

class PdfService: 

    @staticmethod
    def pdf_to_text(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        return text

    @staticmethod
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





    @staticmethod
    def anonymize_and_assign(article_id):
        print("Starting anonymize_and_assign...")

        article = Article.query.filter_by(id=article_id).first()
        if not article:
            return {"error": "Article not found"}, 404

        
        base_filename = os.path.basename(article.original_pdf_path)
        destination_path = os.path.join(ANONYMIZED_FOLDER, base_filename)

        shutil.copy(article.original_pdf_path, destination_path)

        
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
            "message": "Article was anonymized and assigned to reviewer with id=2.",
            "assigned_reviewer_id": reviewer_id,
            "anonymized_path": destination_path
        }, 200
        

    
    @staticmethod
    def merge_and_save_pdf(review_text, article):
        input_path = article.original_pdf_path
        output_filename = os.path.basename(input_path)
        output_path = os.path.join(REVIEWS_FOLDER, output_filename)
        
        review_text = "Reviewer Notes: "+ review_text 
    
        os.makedirs(REVIEWS_FOLDER, exist_ok=True)
    
        with open(input_path, "rb") as file:
            input_pdf = PdfReader(file)
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
            
            article.review_pdf_path = output_path
            db.session.add(article)
            db.session.commit()
    
        with open(output_path, "wb") as outputStream:
            output_pdf.write(outputStream)
            

        
        

    
    

