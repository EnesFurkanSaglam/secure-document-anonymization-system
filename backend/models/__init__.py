from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


from .user import User
from .article import Article
from .assignment import ArticleAssignment
from .review import Review
from .message import Message
from .log import Log


__all__= [
    "db",
    "User",
    "Article",
    "ArticleAssignment",
    "Review",
    "Message",
    "Log"
]