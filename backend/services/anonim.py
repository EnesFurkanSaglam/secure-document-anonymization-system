import fitz
import spacy
import re

def extract_text_from_pdf(pdf_path):
    
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def find_first_person_name_and_extract_context(text):
    
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    print("Bulunan kişi isimleri:", person_names)
    
    if person_names:
        first_person = person_names[0]
        start_index = text.find(first_person)
        if start_index != -1:
            abstract_index = text.lower().find("abstract", start_index)
            if abstract_index != -1:
                context_text = text[start_index:abstract_index]
            else:
                context_text = text[start_index:]
            return first_person, context_text
    return None, None

def get_entities_ensemble(text):

    
    nlp_lg = spacy.load("en_core_web_lg")
    nlp_trf = spacy.load("en_core_web_trf")
    
    entities = set()
    excluded = {"eeg", "ieee"}
    
    for nlp_model in [nlp_lg, nlp_trf]:
        doc = nlp_model(text)
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"]:
                ent_text = ent.text.strip()
                
                if ent_text.lower() not in excluded:
                    entities.add(ent_text)
    return entities


def find_emails(text):

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'
    emails_found = re.findall(email_pattern, text)
    
    return set(emails_found)

def censor_pdf(pdf_path, words_to_censor, output_pdf_path):

    doc = fitz.open(pdf_path)
    for page in doc:
        for word in words_to_censor:
            
            rects = page.search_for(word)
            for rect in rects:
                
                page.add_redact_annot(rect, fill=(1, 1, 1))
        page.apply_redactions()
    doc.save(output_pdf_path)
    print(f"Sansürlenmiş PDF kaydedildi: {output_pdf_path}")