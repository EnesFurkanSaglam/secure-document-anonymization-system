import os
from flask import Flask, send_from_directory, abort
from models import db
from routes import author_bp, editor_bp, reviewer_bp
from flask_cors import CORS
from config import ORIGINAL_FOLDER,ANONYMIZED_FOLDER,REVIEWS_FOLDER,PUBLISHED_FOLDER


def create_app():
    app = Flask(__name__)
    
    CORS(app)  

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_dir = os.path.join(basedir, "database")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "database.sqlite")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    with app.app_context():
        db.create_all()

   
    @app.route('/pdf/<path:filename>')
    def serve_pdf(filename):
        file_path = os.path.join(ORIGINAL_FOLDER, filename)
        if os.path.exists(file_path):
            return send_from_directory(ORIGINAL_FOLDER, filename)
        else:
            abort(404)
    
    @app.route('/pdf/anonym/<path:filename>')
    def serve_anonym_pdf(filename):
        file_path = os.path.join(ANONYMIZED_FOLDER, filename)
        if os.path.exists(file_path):
            return send_from_directory(ANONYMIZED_FOLDER, filename)
        else:
            abort(404)
            
    @app.route('/pdf/rewiev/<path:filename>')
    def serve_rewiev_pdf(filename):
        file_path = os.path.join(REVIEWS_FOLDER, filename)
        if os.path.exists(file_path):
            return send_from_directory(REVIEWS_FOLDER, filename)
        else:
            abort(404)
    
    @app.route('/pdf/publish/<path:filename>')
    def serve_publish_pdf(filename):
        file_path = os.path.join(PUBLISHED_FOLDER, filename)
        if os.path.exists(file_path):
            return send_from_directory(PUBLISHED_FOLDER, filename)
        else:
            abort(404)
    
    
    app.register_blueprint(author_bp, url_prefix="/author")
    app.register_blueprint(editor_bp, url_prefix="/editor")
    app.register_blueprint(reviewer_bp, url_prefix="/reviewer")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
