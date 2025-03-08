from .author_service import AuthorService
from .reviewer_service import ReviewerService
from .editor_service import EditorService

author_service = AuthorService()
reviewer_service = ReviewerService()
editor_service = EditorService()


__all__ = ["author_service","reviewer_service","editor_service"]
