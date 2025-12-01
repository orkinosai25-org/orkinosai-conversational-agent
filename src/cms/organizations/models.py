"""
Organization domain models

Data models for multi-tenant organization management.
To be copied from orkinosaicms.
"""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import Field
from ..base import BaseEntity


class OrganizationStatus(str, Enum):
    """Organization status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TRIAL = "trial"


class Organization(BaseEntity):
    """
    Organization entity
    
    Represents a tenant organization in the multi-tenant system.
    """
    name: str
    slug: str  # URL-friendly identifier
    description: Optional[str] = None
    status: OrganizationStatus = OrganizationStatus.ACTIVE
    owner_id: str  # User ID of the organization owner
    parent_org_id: Optional[str] = None  # For organization hierarchy
    settings: Dict[str, Any] = Field(default_factory=dict)
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    max_members: int = 10  # Maximum allowed members
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True


class OrganizationMember(BaseEntity):
    """
    Organization member association
    
    Links users to organizations with their roles.
    """
    organization_id: str
    user_id: str
    role_id: str  # Role within the organization
    is_primary: bool = False  # User's primary organization
    invitation_accepted: bool = True
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
