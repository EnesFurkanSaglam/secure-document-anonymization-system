import os
import io
from flask import Flask, send_file, abort, send_from_directory
from models import db
from routes import author_bp, editor_bp, reviewer_bp
from flask_cors import CORS
from config import ORIGINAL_FOLDER, ANONYMIZED_FOLDER, REVIEWS_FOLDER, PUBLISHED_FOLDER
from services.encryption_service import EncryptionService
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    
    CORS(app)  
    load_dotenv()

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_dir = os.path.join(basedir, "database")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "database.sqlite")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Şifreleme anahtarını environment'tan alıp EncryptionService'i başlatalım
    ENC_KEY = os.environ.get("ENCRYPTION_KEY")
    if not ENC_KEY:
        raise ValueError("ENCRYPTION_KEY environment variable is not set. Please set it before running.")
    EncryptionService.init(ENC_KEY)

    @app.route('/pdf/<path:filename>')
    def serve_pdf(filename):
        """
        Diskte ORIGINAL_FOLDER altında şifreli PDF saklı.
        Bellekte deşifre edip tarayıcıya gönderir.
        """
        file_path = os.path.join(ORIGINAL_FOLDER, filename)
        if not os.path.exists(file_path):
            abort(404)
        
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        try:
            decrypted_data = EncryptionService.decrypt_data(encrypted_data)
        except Exception:
            abort(404)  # Dosya çözülemiyorsa 404 vs.

        return send_file(
            io.BytesIO(decrypted_data),
            mimetype='application/pdf',
            as_attachment=False,
            download_name=filename
        )

    @app.route('/pdf/anonym/<path:filename>')
    def serve_anonym_pdf(filename):
        """
        Diskte ANONYMIZED_FOLDER altında şifreli PDF saklı.
        Bellekte deşifre edip tarayıcıya gönderir.
        """
        file_path = os.path.join(ANONYMIZED_FOLDER, filename)
        if not os.path.exists(file_path):
            abort(404)

        with open(file_path, "rb") as f:
            enc_data = f.read()
        try:
            dec_data = EncryptionService.decrypt_data(enc_data)
        except Exception:
            abort(404)

        return send_file(
            io.BytesIO(dec_data),
            mimetype='application/pdf',
            as_attachment=False,
            download_name=filename
        )
    
    @app.route('/pdf/rewiev/<path:filename>')
    def serve_rewiev_pdf(filename):
        """
        Diskte REVIEWS_FOLDER altında şifreli PDF saklı.
        Bellekte deşifre edip tarayıcıya gönderir.
        """
        file_path = os.path.join(REVIEWS_FOLDER, filename)
        if not os.path.exists(file_path):
            abort(404)

        with open(file_path, "rb") as f:
            enc_data = f.read()
        try:
            dec_data = EncryptionService.decrypt_data(enc_data)
        except Exception:
            abort(404)

        return send_file(
            io.BytesIO(dec_data),
            mimetype='application/pdf',
            as_attachment=False,
            download_name=filename
        )

    @app.route('/pdf/publish/<path:filename>')
    def serve_publish_pdf(filename):
        """
        Bu rotada 'published' dosyalar düz PDF olarak saklanıyor. 
        O yüzden yine send_from_directory ile ham PDF dönüyoruz.
        """
        file_path = os.path.join(PUBLISHED_FOLDER, filename)
        if os.path.exists(file_path):
            return send_from_directory(PUBLISHED_FOLDER, filename)
        else:
            abort(404)

    # Blueprint registration
    app.register_blueprint(author_bp, url_prefix="/author")
    app.register_blueprint(editor_bp, url_prefix="/editor")
    app.register_blueprint(reviewer_bp, url_prefix="/reviewer")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
