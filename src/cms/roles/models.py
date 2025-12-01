"""
Role and Permission models

Data models for RBAC system.
To be copied from orkinosaicms.
"""

from typing import Optional, List
from pydantic import Field
from ..base import BaseEntity


class Permission(BaseEntity):
    """
    Permission entity
    
    Represents a specific permission/capability in the system.
    """
    name: str
    code: str  # Unique permission code (e.g., "user.create", "document.delete")
    description: Optional[str] = None
    resource: str  # The resource this permission applies to (e.g., "user", "document")
    action: str  # The action allowed (e.g., "create", "read", "update", "delete")
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True


class Role(BaseEntity):
    """
    Role entity
    
    Represents a role that groups permissions.
    """
    name: str
    code: str  # Unique role code (e.g., "admin", "editor", "viewer")
    description: Optional[str] = None
    is_system_role: bool = False  # System roles cannot be deleted
    permission_codes: List[str] = Field(default_factory=list)  # List of permission codes
    parent_role_id: Optional[str] = None  # For role hierarchy
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True


class RolePermission(BaseEntity):
    """
    Role-Permission association
    
    Links roles to their permissions.
    """
    role_id: str
    permission_id: str
    granted: bool = True  # False for explicit deny
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
