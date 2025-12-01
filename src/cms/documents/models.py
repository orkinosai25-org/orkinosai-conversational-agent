"""Document models - To be copied from orkinosaicms"""

from typing import Optional
from ..base import BaseEntity


class Document(BaseEntity):
    """Document entity"""
    name: str
    file_path: str
    file_size: int
    mime_type: str
    organization_id: str
    uploaded_by: str
    is_public: bool = False


class DocumentVersion(BaseEntity):
    """Document version tracking"""
    document_id: str
    version_number: int
    file_path: str
    file_size: int
    comment: Optional[str] = None
