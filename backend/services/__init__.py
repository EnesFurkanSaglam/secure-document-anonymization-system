from .anon_service import AnonService
from .author_service import AuthorService
from .file_service import FileService

anon_service = AnonService()
author_service = AuthorService()
file_service = FileService()


__all__ = ["anon_service", "author_service", "file_service"]
