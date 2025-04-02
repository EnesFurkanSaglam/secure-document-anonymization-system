import fitz
import spacy
import re
from datetime import datetime
from models import LabelText,db
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from dotenv import load_dotenv
import os

load_dotenv()
AES_SECRET_KEY = os.getenv("AES_SECRET_KEY").encode("utf-8")


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
    import spacy

    nlp_lg = spacy.load("en_core_web_lg")
    nlp_trf = spacy.load("en_core_web_trf")

    # Genişletilmiş İngilizce excluded listesi
    excluded = set(map(str.lower, {
        # AI & ML
        "deep learning", "machine learning", "generative ai", "neural networks",
        "transformer", "bert", "gpt", "llm", "rnn", "cnn", "lstm", "vae", "gan",
        "reinforcement learning", "supervised learning", "unsupervised learning",
        "zero-shot learning", "few-shot learning", "transfer learning",

        # NLP
        "nlp", "natural language processing", "pos tagging", "ner", "lemmatization",
        "tokenization", "dependency parsing", "coreference resolution", "word2vec", "glove",
        "sentence embedding", "text summarization", "text classification", "question answering",

        # Computer Vision
        "computer vision", "image classification", "object detection", "segmentation",
        "yolo", "faster rcnn", "ssd", "resnet", "imagenet", "openpose",

        # Data Science & Viz
        "data mining", "data visualization", "tsne", "pca", "hadoop", "spark", "tableau",
        "power bi", "matplotlib", "seaborn", "plotly", "bokeh", "timeseries analysis",
        "big data", "etl", "data warehouse",

        # UI/UX, BCI, AR/VR
        "bci", "brain-computer interface", "user experience design", "ux", "ui",
        "ar", "vr", "augmented reality", "virtual reality", "xr", "hci", "oculus", "hololens",

        # Cybersecurity
        "encryption algorithms", "aes", "rsa", "ecc", "hashing", "sha256", "md5",
        "public key", "private key", "digital forensics", "authentication systems",
        "penetration testing", "network security", "malware", "phishing", "zero-day", "xss", "csrf",

        # Secure Development
        "secure software development", "owasp", "code injection", "buffer overflow",
        "input validation", "access control", "vulnerability", "threat modeling",

        # Networks, Cloud, Distributed Systems
        "5g", "next-generation networks", "cloud computing", "distributed systems",
        "edge computing", "fog computing", "aws", "azure", "gcp", "virtual machines",
        "containers", "kubernetes", "docker",

        # Blockchain
        "blockchain", "p2p", "decentralized systems", "ethereum", "smart contracts",
        "consensus algorithms", "bitcoin", "ipfs", "dapps", "solidity", "web3",

        # Extra tech/platforms/tools
        "ieee", "eeg", "json", "html", "css", "http", "https", "api", "sdk",
        "ssh", "dns", "ftp", "sql", "nosql", "jwt", "yaml", "csv", "docx", "pptx",
        "github", "gitlab", "stackoverflow", "huggingface", "openai"
    }))

    entities = set()

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
    
    key = AES_SECRET_KEY

    def pad(text):
        padding_len = 16 - len(text) % 16
        return text + chr(padding_len) * padding_len

    def encrypt_text(plain_text):
        plain_text = pad(plain_text)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(plain_text.encode("utf-8"))
        return base64.b64encode(iv + encrypted).decode("utf-8")

    nlp = spacy.load("en_core_web_lg")
    author_counter = 1
    org_counter = 1
    mail_counter = 1

    doc = fitz.open(pdf_path)
    for page in doc:
        for word in words_to_censor:
            entity_label = None
            if "@" in word:
                entity_label = "MAIL"
            else:
                temp_doc = nlp(word)
                for ent in temp_doc.ents:
                    if ent.text.strip() == word.strip():
                        if ent.label_ == "PERSON":
                            entity_label = "AUTHOR"
                        elif ent.label_ == "ORG":
                            entity_label = "ORG"
                        break
            if entity_label is None:
                entity_label = "CENSORED"

            rects = page.search_for(word)
            for rect in rects:
                if entity_label == "AUTHOR":
                    label = f"AUTHOR{author_counter}"
                    author_counter += 1
                elif entity_label == "ORG":
                    label = f"ORG{org_counter}"
                    org_counter += 1
                elif entity_label == "MAIL":
                    label = f"MAIL{mail_counter}"
                    mail_counter += 1
                else:
                    label = "CENSORED"

                encrypted_text = encrypt_text(word)

                new_entry = LabelText(
                    label=label,
                    text=encrypted_text,
                    x=rect.x0,
                    y=rect.y0,
                    width=rect.width,
                    height=rect.height,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(new_entry)
                page.add_redact_annot(rect, fill=(1, 1, 1))
        page.apply_redactions()

    doc.save(output_pdf_path)
    db.session.commit()
