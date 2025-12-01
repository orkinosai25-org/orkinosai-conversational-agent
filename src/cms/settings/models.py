"""Settings models - To be copied from orkinosaicms"""

from typing import Optional, Any
from ..base import BaseEntity


class Setting(BaseEntity):
    """Setting entity"""
    key: str
    value: Any
    scope: str = "system"  # system, organization, user
    scope_id: Optional[str] = None  # organization_id or user_id
    is_encrypted: bool = False
    description: Optional[str] = None
