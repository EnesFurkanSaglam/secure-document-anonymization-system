from .author_service import AuthorService
from .reviewer_service import ReviewerService
from .editor_service import EditorService
from .pdf_service import PdfService

author_service = AuthorService()
reviewer_service = ReviewerService()
editor_service = EditorService()
pdf_service = PdfService()


__all__ = ["author_service","reviewer_service","editor_service","pdf_service"]
