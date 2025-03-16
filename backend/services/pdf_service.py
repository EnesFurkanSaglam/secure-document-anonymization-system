import fitz  # PyMuPDF
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

def pdf_to_text(pdf_path):
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


def anonymize_and_assign(pdf_path):
    print("")
    
    ##Anonimleştirme işlemleri ve atama işlemleri şu anlık id si iki olan hakeme atanıyor 
    
    

