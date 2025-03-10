import os
from flask import Flask
from models import db
from routes import author_bp, editor_bp, reviewer_bp
from flask_cors import CORS

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

    app.register_blueprint(author_bp, url_prefix="/author")
    app.register_blueprint(editor_bp, url_prefix="/editor")
    app.register_blueprint(reviewer_bp, url_prefix="/reviewer")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
