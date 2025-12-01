"""Sync models - To be copied from orkinosaicms"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import Field
from ..base import BaseEntity


class SyncJob(BaseEntity):
    """Data synchronization job"""
    name: str
    source_system: str
    target_system: str
    status: str = "pending"  # pending, running, completed, failed
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    records_processed: int = 0
    records_failed: int = 0
    error_message: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
