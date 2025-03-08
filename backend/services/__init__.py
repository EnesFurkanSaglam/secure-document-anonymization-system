from .anon_service import AnonService
from .author_service import AuthorService
from .file_service import FileService
from .reviewer_service import ReviweverService
from .editor_service import EditorService

anon_service = AnonService()
author_service = AuthorService()
file_service = FileService()
reviewer_service = ReviweverService()
editor_service = EditorService()


__all__ = ["anon_service", "author_service", "file_service","reviewer_service","editor_service"]
