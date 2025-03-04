from flask import Flask
from models import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)