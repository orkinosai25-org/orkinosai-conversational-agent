"""Document service - To be copied from orkinosaicms"""

from ..base import ServiceResponse


class DocumentService:
    """Document management service - Placeholder"""
    
    def upload_document(self, file_data, **kwargs) -> ServiceResponse:
        """Upload a document"""
        raise NotImplementedError("To be implemented when copied from orkinosaicms")
    
    def download_document(self, document_id: str) -> bytes:
        """Download document content"""
        raise NotImplementedError("To be implemented when copied from orkinosaicms")
