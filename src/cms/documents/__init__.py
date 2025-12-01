"""
Document Management Module

Generic file upload, storage, and retrieval (non-AI-specific).
Source: To be copied from orkinosaicms
"""

from .models import Document, DocumentVersion
from .services import DocumentService

__all__ = ['Document', 'DocumentVersion', 'DocumentService']
