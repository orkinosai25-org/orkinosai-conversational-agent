"""Sync service - To be copied from orkinosaicms"""

from ..base import ServiceResponse


class SyncService:
    """Data synchronization service - Placeholder"""
    
    def create_sync_job(self, name: str, source: str, target: str) -> ServiceResponse:
        """Create a sync job"""
        raise NotImplementedError("To be implemented when copied from orkinosaicms")
    
    def run_sync_job(self, job_id: str) -> ServiceResponse:
        """Execute a sync job"""
        raise NotImplementedError("To be implemented when copied from orkinosaicms")
