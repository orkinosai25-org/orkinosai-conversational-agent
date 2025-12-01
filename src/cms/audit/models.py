"""Audit models - To be copied from orkinosaicms"""

from typing import Optional, Dict, Any
from pydantic import Field
from ..base import BaseEntity


class AuditLog(BaseEntity):
    """Audit log entry"""
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    changes: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
