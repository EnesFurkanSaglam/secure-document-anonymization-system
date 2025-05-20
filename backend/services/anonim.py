import fitz
import spacy
import re
from models import db
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64
from dotenv import load_dotenv
import os

load_dotenv()
AES_SECRET_KEY = os.getenv("AES_SECRET_KEY").encode("utf-8")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text("text") for page in doc)


def find_first_person_name_and_extract_context(text):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    if person_names:
        first_person = person_names[0]
        start_index = text.find(first_person)
        if start_index != -1:
            abstract_index = text.lower().find("abstract", start_index)
            context_text = text[start_index:abstract_index] if abstract_index != -1 else text[start_index:]
            return first_person, context_text
    return None, None


def get_entities_ensemble(text):
    nlp_lg = spacy.load("en_core_web_lg")
    nlp_trf = spacy.load("en_core_web_trf")

    excluded = {
        "deep learning", "machine learning", "generative ai", "neural networks", "transformer", "bert", "gpt", "llm",
        "rnn", "cnn", "lstm", "vae", "gan", "reinforcement learning", "supervised learning", "unsupervised learning",
        "zero-shot learning", "few-shot learning", "transfer learning", "nlp", "natural language processing",
        "pos tagging", "ner", "lemmatization", "tokenization", "dependency parsing", "coreference resolution",
        "word2vec", "glove", "sentence embedding", "text summarization", "text classification", "question answering",
        "computer vision", "image classification", "object detection", "segmentation", "yolo", "faster rcnn", "ssd",
        "resnet", "imagenet", "openpose", "data mining", "data visualization", "tsne", "pca", "hadoop", "spark",
        "tableau", "power bi", "matplotlib", "seaborn", "plotly", "bokeh", "timeseries analysis", "big data", "etl",
        "data warehouse", "bci", "brain-computer interface", "user experience design", "ux", "ui", "ar", "vr",
        "augmented reality", "virtual reality", "xr", "hci", "oculus", "hololens", "encryption algorithms", "aes",
        "rsa", "ecc", "hashing", "sha256", "md5", "public key", "private key", "digital forensics",
        "authentication systems", "penetration testing", "network security", "malware", "phishing", "zero-day",
        "xss", "csrf", "secure software development", "owasp", "code injection", "buffer overflow", "input validation",
        "access control", "vulnerability", "threat modeling", "5g", "next-generation networks", "cloud computing",
        "distributed systems", "edge computing", "fog computing", "aws", "azure", "gcp", "virtual machines",
        "containers", "kubernetes", "docker", "blockchain", "p2p", "decentralized systems", "ethereum",
        "smart contracts", "consensus algorithms", "bitcoin", "ipfs", "dapps", "solidity", "web3", "ieee", "eeg",
        "json", "html", "css", "http", "https", "api", "sdk", "ssh", "dns", "ftp", "sql", "nosql", "jwt", "yaml",
        "csv", "docx", "pptx", "github", "gitlab", "stackoverflow", "huggingface", "openai"
    }

    entities = set()
    for nlp_model in [nlp_lg, nlp_trf]:
        doc = nlp_model(text)
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"] and ent.text.lower().strip() not in excluded:
                entities.add(ent.text.strip())

    return entities


def find_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'
    return set(re.findall(email_pattern, text))


def encrypt_text(plain_text, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(plain_text.encode("utf-8"), AES.block_size)
    encrypted = cipher.encrypt(padded_text)
    return base64.b64encode(iv + encrypted).decode("utf-8")


def censor_pdf(pdf_path, words_to_censor, output_pdf_path):
    nlp = spacy.load("en_core_web_lg")

    author_counter = 1
    org_counter = 1
    mail_counter = 1

    doc = fitz.open(pdf_path)

    for page in doc:
        for word in words_to_censor:
            if "@" in word:
                entity_label = "MAIL"
            else:
                temp_doc = nlp(word)
                entity_label = next((
                    "AUTHOR" if ent.label_ == "PERSON"
                    else "ORG" if ent.label_ == "ORG"
                    else "CENSORED"
                    for ent in temp_doc.ents
                    if ent.text.strip() == word.strip()
                ), "CENSORED")

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

                encrypted_text = encrypt_text(word, AES_SECRET_KEY)
                page.add_redact_annot(rect, fill=(1, 1, 1))

        page.apply_redactions()

    doc.save(output_pdf_path)
    db.session.commit()
