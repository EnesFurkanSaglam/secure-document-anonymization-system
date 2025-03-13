import os

BASE_UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
ORIGINAL_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "original")
ANONYMIZED_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "anonymized")
REVIEWS_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "reviews")

os.makedirs(ORIGINAL_FOLDER, exist_ok=True)
os.makedirs(ANONYMIZED_FOLDER, exist_ok=True)
os.makedirs(REVIEWS_FOLDER, exist_ok=True)
